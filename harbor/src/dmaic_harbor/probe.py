"""Provider liveness probe: find out who can actually answer, before the sweep starts.

WHY THIS EXISTS
---------------
Balance exhaustion was the single largest cause of lost trials in the last campaign. One
provider was suspended part-way through; another answered ``HTTP 402 Insufficient
Balance`` to 923 consecutive requests; a gateway reported that its upstream accounts were
exhausted. None of that is a model result, and all of it was discovered by watching a
run fail rather than by asking first.

The asymmetry is the whole argument. A campaign that discovers an empty account at trial
400 has spent 400 trials of wall clock and budget to learn something that costs a handful
of tokens to ask directly. So: ask directly, once, before the first trial.

WHAT IT ANSWERS, PER CONFIGURED MODEL
-------------------------------------
* **reachable**  -- the endpoint resolves, connects and speaks HTTP
* **auth-ok**    -- this credential is accepted for this model
* **has-balance**-- the account behind it can currently be charged

Those are three different failures with three different fixes, and a run that lumps them
into "the model scored 0" cannot tell you which one you have.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
* It does not read the credential file. It reads the *environment*, which the launcher
  has already populated from that file, so the probe never opens a credential at rest.
* It never prints, logs, returns or embeds a credential. Every response body passes
  through :func:`redact` before it can reach a message, keyed on the live values of the
  configured variables -- so even a provider that echoes the key back in an error string
  cannot leak it through this tool.
* It puts no credential on a command line or in a URL. Headers only.
* It hardcodes no provider, no endpoint and no model name. The target list is operator
  configuration kept beside the credential file, outside this repository -- which is both
  the disclosure rule and the reason this probe works for a campaign whose contestant list
  it has never heard of.

COST
----
One request per configured model, ``max_tokens`` = :data:`PROBE_MAX_TOKENS` (default 1),
with a one-character prompt. That is the smallest chargeable unit any of these APIs
sells. ``--dry-run`` sends nothing at all and prints the plan, which is how this module
was developed and how it is tested: the whole classification matrix is exercised against
a local stub and an invalid credential, so both the success and the failure path are
proven without spending anything.

CONFIGURATION
-------------
A JSON file, resolved from ``$DMAIC_PROVIDERS_FILE`` or from ``providers.json`` beside the
credential file::

    {
      "providers": [
        {
          "id": "gateway-a",
          "wire": "openai",
          "base_url_env": "SOME_API_BASE",
          "api_key_env": "SOME_API_KEY",
          "models": ["model-one", "model-two"]
        },
        {
          "id": "gateway-b",
          "wire": "anthropic",
          "base_url_env": "OTHER_GW_BASE",
          "api_key_env": "OTHER_GW_KEY",
          "models": ["model-three"]
        }
      ]
    }

``wire`` selects the request shape only (``openai`` -> ``POST {base}/chat/completions``,
``anthropic`` -> ``POST {base}/v1/messages``); it names a protocol, not a vendor. Several
providers commonly sit behind one ``openai`` wire on different bases, which is exactly why
the base URL and the credential are named per entry rather than assumed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

try:  # pragma: no cover
    from .preflight import ENV_FILE_VAR, resolve_env_file
except ImportError:  # pragma: no cover - direct-script execution
    from preflight import ENV_FILE_VAR, resolve_env_file  # type: ignore[no-redef]


# --------------------------------------------------------------------------- config

PROVIDERS_FILE_VAR = "DMAIC_PROVIDERS_FILE"
DEFAULT_PROVIDERS_BASENAME = "providers.json"

#: The whole point is that this is the smallest request the API will bill for.
PROBE_MAX_TOKENS = 1
PROBE_PROMPT = "1"
DEFAULT_TIMEOUT_S = 30
DEFAULT_RETRIES = 2

#: Some gateways sit behind a WAF that bans the DEFAULT Python user agent by client signature
#: and answers `403 error code: 1010`. Measured on this machine: identical URL, headers and body
#: to a request curl makes successfully; `Python-urllib/3.12` -> 403, `curl/8.7.1` -> 200. The
#: probe must send what the campaign's own client sends, or it certifies a provider the campaign
#: then cannot reach -- and a WAF block would be recorded as trials the model failed.
PROBE_USER_AGENT = "curl/8.7.1"

ANTHROPIC_VERSION = "2023-06-01"

WIRES = ("openai", "anthropic")

# --------------------------------------------------------------------------- verdicts

OK = "ok"                       # reachable, auth-ok, has-balance
NO_BALANCE = "no_balance"       # reachable, auth-ok, cannot be charged
EXHAUSTED = "exhausted"         # a gateway's upstream pool is empty -- often transient
AUTH_FAILED = "auth_failed"     # reachable, credential rejected
RATE_LIMITED = "rate_limited"   # reachable, auth-ok, throttled right now
UNREACHABLE = "unreachable"     # DNS / connect / TLS / timeout
HTTP_ERROR = "http_error"       # reachable, but an unclassified status
NO_CREDENTIAL = "no_credential" # the configured variable is unset or empty
MISCONFIGURED = "misconfigured" # the config entry itself is wrong
NOT_PROBED = "not_probed"       # --dry-run

#: Verdicts that must stop a campaign before it starts. A rate limit is not one of them --
#: it is a throughput problem, and the harness already retries. An empty account is: no
#: amount of retrying fills it, and every trial that runs into it is a lost trial.
FATAL = (NO_BALANCE, AUTH_FAILED, UNREACHABLE, HTTP_ERROR, NO_CREDENTIAL, MISCONFIGURED)

#: Reported, and loud, but not fatal on their own: an exhausted upstream pool has been
#: observed to clear on retry, and is categorically different from an authorisation
#: failure that never clears. Recording either as "the model scored 0" is the error this
#: whole module exists to prevent.
DEGRADED = (EXHAUSTED, RATE_LIMITED)

#: Body substrings that mean "the account cannot be charged", lowercased. Providers signal
#: this with wildly inconsistent status codes -- 401, 402, 403, 429 and 200-with-an-error
#: body have all been observed -- so the body text is load-bearing, not a nicety.
_BALANCE_PATTERNS = (
    "insufficient balance", "insufficient_quota", "insufficient quota",
    "exceeded your current quota", "billing", "balance is not enough",
    "not enough balance", "arrears", "arrearage", "payment required",
    "out of credit", "no credit", "credit exhausted", "recharge",
)

#: Body substrings that mean "a shared upstream pool is empty right now".
_EXHAUSTED_PATTERNS = (
    "accounts exhausted", "account exhausted", "no available account",
    "all available accounts", "upstream exhausted", "no available channel",
)

#: Body substrings that mean "this credential is not accepted".
_AUTH_PATTERNS = (
    "invalid api key", "incorrect api key", "invalid_api_key", "unauthorized",
    "authentication", "invalid token", "api key not valid", "forbidden",
    "access forbidden", "permission denied",
)


# --------------------------------------------------------------------------- redaction

def redact(text: str, secrets: list[str]) -> str:
    """Remove every configured credential value from *text*.

    Applied to EVERY provider-supplied string before it can reach a message, a log line or
    a JSON report. Providers do echo credentials back inside error strings, and an error
    string is precisely what this tool is built to display.

    Long secrets are replaced first so that a short one which happens to be a substring of
    a long one cannot leave the long one partially visible.
    """
    if not text:
        return text
    for value in sorted({s for s in secrets if s and len(s) >= 4}, key=len, reverse=True):
        text = text.replace(value, "<redacted>")
    return text


# --------------------------------------------------------------------------- model

@dataclass
class Target:
    provider_id: str
    wire: str
    base_url: str
    api_key: str          # never rendered; only ever placed in a request header
    key_env: str
    model: str

    @property
    def label(self) -> str:
        return f"{self.provider_id}/{self.model}"


@dataclass
class Probe:
    provider_id: str
    model: str
    verdict: str
    status_code: int | None = None
    latency_ms: int | None = None
    note: str = ""
    attempts: int = 1

    @property
    def reachable(self) -> bool:
        return self.verdict not in (UNREACHABLE, NO_CREDENTIAL, MISCONFIGURED, NOT_PROBED)

    @property
    def auth_ok(self) -> bool:
        return self.verdict in (OK, NO_BALANCE, RATE_LIMITED, EXHAUSTED)

    @property
    def has_balance(self) -> bool | None:
        if self.verdict == OK:
            return True
        if self.verdict == NO_BALANCE:
            return False
        return None

    @property
    def fatal(self) -> bool:
        return self.verdict in FATAL

    def to_dict(self) -> dict:
        return {"provider": self.provider_id, "model": self.model, "verdict": self.verdict,
                "reachable": self.reachable, "auth_ok": self.auth_ok,
                "has_balance": self.has_balance, "status_code": self.status_code,
                "latency_ms": self.latency_ms, "attempts": self.attempts,
                "note": self.note}


# --------------------------------------------------------------------------- config load

def resolve_providers_file(env: dict) -> Path:
    override = env.get(PROVIDERS_FILE_VAR, "").strip()
    if override:
        return Path(override).expanduser()
    return resolve_env_file(env).parent / DEFAULT_PROVIDERS_BASENAME


def load_targets(config: dict, env: dict) -> tuple[list[Target], list[Probe]]:
    """Config + environment -> probeable targets, plus a verdict for each unprobeable one.

    An entry whose credential variable is unset is NOT silently dropped: "you did not
    configure this" and "this is broken" are different operator actions, and a probe that
    reports only what it managed to reach reports the wrong thing.
    """
    targets: list[Target] = []
    problems: list[Probe] = []
    entries = config.get("providers")
    if not isinstance(entries, list):
        return targets, [Probe("<config>", "-", MISCONFIGURED,
                               note="top-level key `providers` must be a list")]

    for i, entry in enumerate(entries):
        pid = str(entry.get("id") or f"provider-{i}") if isinstance(entry, dict) else f"provider-{i}"
        if not isinstance(entry, dict):
            problems.append(Probe(pid, "-", MISCONFIGURED, note="entry is not an object"))
            continue
        wire = str(entry.get("wire", "openai"))
        models = entry.get("models") or []
        if wire not in WIRES:
            problems.append(Probe(pid, "-", MISCONFIGURED,
                                  note=f"wire {wire!r} is not one of {'/'.join(WIRES)}"))
            continue
        if not isinstance(models, list) or not models:
            problems.append(Probe(pid, "-", MISCONFIGURED, note="`models` must be a non-empty list"))
            continue
        base_env = entry.get("base_url_env")
        key_env = entry.get("api_key_env")
        if not base_env or not key_env:
            problems.append(Probe(pid, "-", MISCONFIGURED,
                                  note="`base_url_env` and `api_key_env` are both required"))
            continue
        base = (env.get(str(base_env)) or "").strip().rstrip("/")
        key = (env.get(str(key_env)) or "").strip()
        if not base:
            problems.append(Probe(pid, "-", NO_CREDENTIAL,
                                  note=f"${base_env} is unset or empty"))
            continue
        if not key:
            problems.append(Probe(pid, "-", NO_CREDENTIAL,
                                  note=f"${key_env} is unset or empty"))
            continue
        for model in models:
            targets.append(Target(pid, wire, base, key, str(key_env), str(model)))
    return targets, problems


# --------------------------------------------------------------------------- request

def build_request(t: Target) -> tuple[str, dict, dict]:
    """``(url, headers, body)`` for the smallest chargeable request on this wire.

    Returned rather than sent, so a test can assert the shape -- including that the
    credential appears in a header and nowhere else -- without a network.
    """
    if t.wire == "anthropic":
        url = f"{t.base_url}/v1/messages"
        headers = {"content-type": "application/json",
                   "x-api-key": t.api_key,
                   "anthropic-version": ANTHROPIC_VERSION,
                   "user-agent": PROBE_USER_AGENT}
        body = {"model": t.model, "max_tokens": PROBE_MAX_TOKENS,
                "messages": [{"role": "user", "content": PROBE_PROMPT}]}
    else:
        url = f"{t.base_url}/chat/completions"
        headers = {"content-type": "application/json",
                   "authorization": f"Bearer {t.api_key}",
                   "user-agent": PROBE_USER_AGENT}
        body = {"model": t.model, "max_tokens": PROBE_MAX_TOKENS,
                "messages": [{"role": "user", "content": PROBE_PROMPT}]}
    return url, headers, body


def classify(status: int | None, body: str) -> tuple[str, str]:
    """``(verdict, note)`` from a status code and an ALREADY-REDACTED body.

    Status alone is not sufficient and never was: the same "you are out of money" has been
    seen as 401, 402, 403, 429 and as a 200 carrying an error object. The body text
    decides first; the status code is the fallback.
    """
    low = (body or "").lower()

    for pat in _EXHAUSTED_PATTERNS:
        if pat in low:
            return EXHAUSTED, "upstream account pool reported empty (often transient)"
    for pat in _BALANCE_PATTERNS:
        if pat in low:
            return NO_BALANCE, "provider reports the account cannot be charged"

    if status == 402:
        return NO_BALANCE, "HTTP 402 Payment Required"
    if status in (401, 403):
        for pat in _AUTH_PATTERNS:
            if pat in low:
                return AUTH_FAILED, f"HTTP {status}: credential rejected"
        return AUTH_FAILED, f"HTTP {status}"
    if status == 429:
        return RATE_LIMITED, "HTTP 429: throttled"
    if status is not None and 200 <= status < 300:
        return OK, ""
    if status is not None and 500 <= status < 600:
        return HTTP_ERROR, f"HTTP {status}: provider-side error"
    if status is not None:
        return HTTP_ERROR, f"HTTP {status}"
    return HTTP_ERROR, "no status"


class Transport:
    """Sends one probe request. Injectable, so every branch is testable offline."""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT_S):
        self.timeout = timeout

    def send(self, url: str, headers: dict, body: dict) -> tuple[int | None, str]:
        """``(status_or_None, body_text)``. A transport failure is ``(None, reason)``."""
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        for k, v in headers.items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.status, resp.read(4096).decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            try:
                text = exc.read(4096).decode("utf-8", "replace")
            except Exception:  # pragma: no cover - defensive
                text = ""
            return exc.code, text
        except urllib.error.URLError as exc:
            return None, f"{type(exc.reason).__name__ if exc.reason else 'URLError'}: {exc.reason}"
        except (TimeoutError, OSError) as exc:
            return None, f"{type(exc).__name__}: {exc}"


def probe_target(t: Target, transport: Transport, secrets: list[str],
                 retries: int = DEFAULT_RETRIES, backoff: float = 1.0,
                 sleep=time.sleep) -> Probe:
    """Probe one model, retrying only what is known to clear on retry.

    An exhausted upstream pool and a rate limit have both been observed to succeed on a
    second attempt. An empty account and a rejected credential never do -- retrying those
    only delays the report, so they return immediately.
    """
    url, headers, body = build_request(t)
    attempts = 0
    last = Probe(t.provider_id, t.model, HTTP_ERROR)
    for attempt in range(retries + 1):
        attempts = attempt + 1
        started = time.monotonic()
        status, raw = transport.send(url, headers, body)
        elapsed = int((time.monotonic() - started) * 1000)
        text = redact(raw, secrets)
        if status is None:
            verdict, note = UNREACHABLE, text[:200]
        else:
            verdict, note = classify(status, text)
            if verdict != OK and text:
                # Carry the provider's OWN words through, redacted. "HTTP 401" alone does
                # not distinguish a wrong key from a key that is right but not entitled to
                # this model, and the operator's next action differs between the two. The
                # redaction is what makes quoting the provider safe -- and gateways do put
                # the offending credential into exactly this string.
                note = f"{note}: {text[:160]}".strip(": ")
        last = Probe(t.provider_id, t.model, verdict, status_code=status,
                     latency_ms=elapsed, note=note, attempts=attempts)
        if verdict not in (EXHAUSTED, RATE_LIMITED, UNREACHABLE) or attempt == retries:
            return last
        sleep(backoff * (2 ** attempt))
    return last


# --------------------------------------------------------------------------- report

@dataclass
class ProbeReport:
    probes: list[Probe] = field(default_factory=list)
    providers_file: str = ""

    @property
    def fatal(self) -> list[Probe]:
        return [p for p in self.probes if p.fatal]

    @property
    def degraded(self) -> list[Probe]:
        return [p for p in self.probes if p.verdict in DEGRADED]

    @property
    def ok(self) -> bool:
        return not self.fatal

    def to_dict(self) -> dict:
        return {"providers_file": self.providers_file, "ok": self.ok,
                "n_ok": sum(1 for p in self.probes if p.verdict == OK),
                "n_fatal": len(self.fatal), "n_degraded": len(self.degraded),
                "probes": [p.to_dict() for p in self.probes]}

    def render(self) -> str:
        lines = ["", "DMAIC-Bench provider liveness probe", "=" * 78,
                 f"config: {self.providers_file}",
                 f"{'model':<38} {'reach':<6} {'auth':<6} {'balance':<8} verdict", "-" * 78]
        for p in sorted(self.probes, key=lambda x: (x.provider_id, x.model)):
            bal = {True: "yes", False: "NO", None: "-"}[p.has_balance]
            lines.append(f"{(p.provider_id + '/' + p.model)[:38]:<38} "
                         f"{'yes' if p.reachable else 'NO':<6} "
                         f"{'yes' if p.auth_ok else 'NO':<6} {bal:<8} {p.verdict}")
            if p.note:
                lines.append(f"{'':<38} {p.note}")
        lines.append("=" * 78)
        if self.fatal:
            lines.append(f"PROBE FAILED: {len(self.fatal)} model(s) cannot serve this campaign")
            for p in self.fatal:
                lines.append(f"  {p.provider_id}/{p.model}: {p.verdict}"
                             + (f" -- {p.note}" if p.note else ""))
            lines.append("")
            lines.append("Balance exhaustion is not a model result. A campaign launched now")
            lines.append("would record these as trials the model failed. Top up, fix the")
            lines.append("credential, or drop the contestant from the job config -- then re-probe.")
        elif self.degraded:
            lines.append("PROBE PASSED, DEGRADED: "
                         + ", ".join(f"{p.provider_id}/{p.model} ({p.verdict})"
                                     for p in self.degraded))
            lines.append("These cleared on retry or are throttled. Watch them; the harness")
            lines.append("retries, but a persistent one will show up as a lost trial.")
        else:
            lines.append(f"PROBE PASSED: {len(self.probes)} model(s) reachable, "
                         "authenticated and fundable")
        lines.append("")
        return "\n".join(lines)


def run_probe(config: dict, env: dict, *, transport: Transport | None = None,
              retries: int = DEFAULT_RETRIES, dry_run: bool = False,
              providers_file: str = "", sleep=time.sleep) -> ProbeReport:
    targets, problems = load_targets(config, env)
    report = ProbeReport(probes=list(problems), providers_file=providers_file)
    secrets = sorted({t.api_key for t in targets})

    if dry_run:
        for t in targets:
            url, _, _ = build_request(t)
            report.probes.append(Probe(
                t.provider_id, t.model, NOT_PROBED,
                note=f"would POST {url} with ${t.key_env} in a header, "
                     f"max_tokens={PROBE_MAX_TOKENS} (nothing was sent)"))
        return report

    transport = transport or Transport()
    for t in targets:
        report.probes.append(probe_target(t, transport, secrets, retries=retries,
                                          sleep=sleep))
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="dmaic-harbor-probe",
        description="Ask every configured model whether it is reachable, authenticated "
                    "and fundable -- before a campaign spends anything finding out.")
    ap.add_argument("--providers", help="path to the providers JSON "
                                        f"(default: ${PROVIDERS_FILE_VAR}, else "
                                        f"{DEFAULT_PROVIDERS_BASENAME} beside ${ENV_FILE_VAR})")
    ap.add_argument("--dry-run", action="store_true",
                    help="send nothing; print exactly what would be requested")
    ap.add_argument("--retries", type=int, default=DEFAULT_RETRIES,
                    help="retries for verdicts known to clear (throttle, empty pool)")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S)
    ap.add_argument("--allow-degraded", action="store_true",
                    help="exit 0 even when a provider is throttled or its pool is empty")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    env = dict(os.environ)
    path = Path(a.providers).expanduser() if a.providers else resolve_providers_file(env)
    if not path.exists():
        msg = (f"no provider config at {path}\n"
               f"Write one there (or point ${PROVIDERS_FILE_VAR} at it). Schema:\n"
               '  {"providers": [{"id": "gateway-a", "wire": "openai",\n'
               '                  "base_url_env": "SOME_API_BASE",\n'
               '                  "api_key_env": "SOME_API_KEY",\n'
               '                  "models": ["model-one"]}]}\n'
               "It names environment VARIABLES, never values, so it carries no secret --\n"
               "but keep it beside the credential file, outside any repository.")
        print(msg, file=sys.stderr)
        return 2
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"cannot read provider config {path}: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2

    report = run_probe(config, env, transport=Transport(timeout=a.timeout),
                       retries=a.retries, dry_run=a.dry_run, providers_file=str(path))
    if a.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.render())
    if report.fatal:
        return 1
    if report.degraded and not a.allow_degraded:
        return 3
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
