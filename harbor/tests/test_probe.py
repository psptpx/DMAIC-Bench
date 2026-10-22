"""The provider liveness probe, proven against a local stub -- never against a paid API.

NO TEST IN THIS FILE CONTACTS A PROVIDER. Both halves of the contract are proven without
spending anything:

* the SUCCESS path, against a stub HTTP server bound to loopback that answers with the
  real wire shapes;
* the FAILURE paths -- empty balance, rejected credential, exhausted upstream pool,
  throttling, an unreachable endpoint -- against the same stub, plus an obviously invalid
  credential, which is the one failure a live endpoint would also give for free.

That matters beyond thrift. The failure paths are what the probe is FOR, and they are the
paths a live-API test would exercise least reliably: nobody empties an account on purpose
to check that the check works.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from dmaic_harbor import probe
from dmaic_harbor.probe import (AUTH_FAILED, EXHAUSTED, HTTP_ERROR, MISCONFIGURED,
                                NO_BALANCE, NO_CREDENTIAL, NOT_PROBED, OK, RATE_LIMITED,
                                UNREACHABLE)

INVALID_KEY = "sk-invalid-000000000000000000000000000000"

#: Verbatim shapes observed in the campaign logs. Reproduced as bytes rather than
#: paraphrased, because the classifier reads the body text and a paraphrase would test
#: the paraphrase.
BODY_INSUFFICIENT_BALANCE = '{"error":{"message":"Insufficient Balance","type":"unknown"}}'
BODY_ACCOUNTS_EXHAUSTED = '{"error":{"message":"All available accounts exhausted"}}'
BODY_FORBIDDEN = '{"error":{"message":"Upstream access forbidden"}}'
BODY_OK = ('{"id":"x","choices":[{"message":{"role":"assistant","content":"1"}}],'
           '"usage":{"prompt_tokens":1,"completion_tokens":1}}')
BODY_OK_ANTHROPIC = ('{"id":"x","type":"message","role":"assistant",'
                     '"content":[{"type":"text","text":"1"}],'
                     '"usage":{"input_tokens":1,"output_tokens":1}}')


# --------------------------------------------------------------------------- stub server

class _Stub(ThreadingHTTPServer):
    daemon_threads = True
    script: dict = {}
    seen: list = []
    hits: dict = {}


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence
        pass

    def do_POST(self):
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length).decode("utf-8")
        try:
            body = json.loads(raw)
        except ValueError:
            body = {}
        model = body.get("model", "")
        self.server.seen.append({
            "path": self.path, "model": model, "body": body,
            "authorization": self.headers.get("authorization"),
            "x_api_key": self.headers.get("x-api-key"),
        })
        n = self.server.hits.get(model, 0)
        self.server.hits[model] = n + 1
        entry = self.server.script.get(model, (404, '{"error":"unknown model"}'))
        # A list means "answer differently on each attempt" -- how a transient failure is
        # reproduced without a sleep.
        if isinstance(entry, list):
            entry = entry[min(n, len(entry) - 1)]
        status, text = entry
        payload = text.encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


@pytest.fixture
def stub():
    server = _Stub(("127.0.0.1", 0), _Handler)
    server.script = {}
    server.seen = []
    server.hits = {}
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    server.base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()


def cfg(models, wire="openai", pid="stub"):
    return {"providers": [{"id": pid, "wire": wire, "base_url_env": "STUB_BASE",
                           "api_key_env": "STUB_KEY", "models": list(models)}]}


def envfor(stub, key=INVALID_KEY):
    return {"STUB_BASE": stub.base_url, "STUB_KEY": key}


def verdicts(report):
    return {f"{p.provider_id}/{p.model}": p.verdict for p in report.probes}


# ============================================================ the three questions

def test_a_live_endpoint_reports_reachable_auth_ok_and_has_balance(stub):
    stub.script = {"good": (200, BODY_OK)}
    report = probe.run_probe(cfg(["good"]), envfor(stub), retries=0)
    p = report.probes[0]
    assert (p.verdict, p.reachable, p.auth_ok, p.has_balance) == (OK, True, True, True)
    assert report.ok


def test_an_empty_account_is_reachable_and_authenticated_but_not_fundable(stub):
    """The distinction the whole module exists for. 402 is not "the model scored 0"."""
    stub.script = {"broke": (402, BODY_INSUFFICIENT_BALANCE)}
    p = probe.run_probe(cfg(["broke"]), envfor(stub), retries=0).probes[0]
    assert p.verdict == NO_BALANCE
    assert p.reachable is True and p.auth_ok is True and p.has_balance is False


def test_a_rejected_credential_is_reachable_but_not_authenticated(stub):
    stub.script = {"nope": (401, '{"error":{"message":"Invalid API key"}}')}
    p = probe.run_probe(cfg(["nope"]), envfor(stub), retries=0).probes[0]
    assert p.verdict == AUTH_FAILED
    assert p.reachable is True and p.auth_ok is False and p.has_balance is None


def test_an_unreachable_endpoint_is_neither(monkeypatch):
    """A closed port: no server was ever started on it."""
    env = {"STUB_BASE": "http://127.0.0.1:9", "STUB_KEY": INVALID_KEY}
    p = probe.run_probe(cfg(["x"]), env, retries=0, sleep=lambda s: None).probes[0]
    assert p.verdict == UNREACHABLE
    assert p.reachable is False and p.auth_ok is False


# ============================================================ the invalid-key path

def test_an_obviously_invalid_key_exercises_the_failure_path_without_spending(stub):
    """This is how a live gateway is safely smoke-tested: a key that cannot possibly be
    billable. Verified here against the stub so the assertion is deterministic."""
    stub.script = {"m": (403, BODY_FORBIDDEN)}
    report = probe.run_probe(cfg(["m"]), envfor(stub, key=INVALID_KEY), retries=0)
    assert report.probes[0].verdict == AUTH_FAILED
    assert not report.ok
    # ...and the key that was rejected is still not in the output.
    assert INVALID_KEY not in report.render()


def test_the_authorisation_failure_that_is_not_a_score_of_zero(stub):
    """An authorisation failure on every attempt is a contestant that cannot compete --
    categorically different from the transient exhausted-pool error the same gateway also
    emits. Recording either as a model result is the error being prevented."""
    stub.script = {"forbidden": (403, BODY_FORBIDDEN)}
    p = probe.run_probe(cfg(["forbidden"]), envfor(stub), retries=2,
                        sleep=lambda s: None).probes[0]
    assert p.verdict == AUTH_FAILED
    assert p.attempts == 1, "an authorisation failure never clears; retrying only delays"


# ============================================================ transient vs terminal

def test_an_exhausted_upstream_pool_is_retried_and_clears(stub):
    stub.script = {"pool": [(502, BODY_ACCOUNTS_EXHAUSTED), (200, BODY_OK)]}
    p = probe.run_probe(cfg(["pool"]), envfor(stub), retries=2,
                        sleep=lambda s: None).probes[0]
    assert p.verdict == OK and p.attempts == 2


def test_a_persistently_exhausted_pool_is_reported_as_degraded_not_fatal(stub):
    stub.script = {"pool": (502, BODY_ACCOUNTS_EXHAUSTED)}
    report = probe.run_probe(cfg(["pool"]), envfor(stub), retries=1, sleep=lambda s: None)
    p = report.probes[0]
    assert p.verdict == EXHAUSTED and p.attempts == 2
    assert not p.fatal, "an exhausted pool has been observed to clear; it is not an empty account"
    assert report.ok and report.degraded


def test_throttling_is_degraded_not_fatal(stub):
    stub.script = {"busy": (429, '{"error":{"message":"Too many requests"}}')}
    report = probe.run_probe(cfg(["busy"]), envfor(stub), retries=0, sleep=lambda s: None)
    assert report.probes[0].verdict == RATE_LIMITED
    assert report.ok


def test_an_empty_account_is_not_retried(stub):
    stub.script = {"broke": (402, BODY_INSUFFICIENT_BALANCE)}
    p = probe.run_probe(cfg(["broke"]), envfor(stub), retries=3,
                        sleep=lambda s: None).probes[0]
    assert p.attempts == 1, "no amount of retrying fills an empty account"


# ============================================================ classification matrix

@pytest.mark.parametrize("status,body,expected", [
    (200, BODY_OK, OK),
    (402, "", NO_BALANCE),
    (401, '{"message":"Insufficient Balance"}', NO_BALANCE),   # body beats status
    (403, '{"message":"insufficient_quota"}', NO_BALANCE),
    (429, '{"message":"You exceeded your current quota"}', NO_BALANCE),
    (200, '{"error":{"message":"Insufficient Balance"}}', NO_BALANCE),  # 200 + error body
    (401, '{"message":"Invalid API key"}', AUTH_FAILED),
    (403, BODY_FORBIDDEN, AUTH_FAILED),
    (429, '{"message":"slow down"}', RATE_LIMITED),
    (502, BODY_ACCOUNTS_EXHAUSTED, EXHAUSTED),
    (500, '{"message":"boom"}', HTTP_ERROR),
    (404, '{"message":"no such model"}', HTTP_ERROR),
])
def test_classification(status, body, expected):
    """Status alone was never sufficient: the same "you are out of money" has arrived as
    401, 402, 403, 429 and as a 200 carrying an error object."""
    assert probe.classify(status, body)[0] == expected


# ============================================================ the credential never leaks

def test_a_provider_that_echoes_the_key_back_still_cannot_leak_it(stub):
    """Gateways do put the offending credential into their error strings, and an error
    string is exactly what this tool prints."""
    key = "sk-super-secret-value-abcdef123456"
    stub.script = {"echo": (401, json.dumps(
        {"error": {"message": f"invalid api key: {key} rejected"}}))}
    report = probe.run_probe(cfg(["echo"]), envfor(stub, key=key), retries=0)
    assert report.probes[0].verdict == AUTH_FAILED
    for blob in (report.render(), json.dumps(report.to_dict()),
                 report.probes[0].note, str(report.probes[0].to_dict())):
        assert key not in blob
    assert "<redacted>" in report.probes[0].note


def test_redact_prefers_the_longest_secret_so_a_prefix_cannot_uncover_it():
    short, long = "abcd1234", "abcd1234-and-more-secret"
    out = probe.redact(f"saw {long} here", [short, long])
    assert long not in out and "and-more-secret" not in out


def test_redact_ignores_trivially_short_values_rather_than_mangling_output():
    assert probe.redact("a normal message", ["a", ""]) == "a normal message"


def test_the_credential_travels_in_a_header_and_never_in_the_url_or_body(stub):
    key = "sk-header-only-abcdef"
    stub.script = {"m": (200, BODY_OK)}
    probe.run_probe(cfg(["m"]), envfor(stub, key=key), retries=0)
    seen = stub.seen[0]
    assert seen["authorization"] == f"Bearer {key}"
    assert key not in seen["path"]
    assert key not in json.dumps(seen["body"])


def test_the_anthropic_wire_uses_its_own_header_and_path(stub):
    key = "sk-ant-abcdef123456"
    stub.script = {"m": (200, BODY_OK_ANTHROPIC)}
    report = probe.run_probe(cfg(["m"], wire="anthropic"), envfor(stub, key=key), retries=0)
    assert report.probes[0].verdict == OK
    seen = stub.seen[0]
    assert seen["path"] == "/v1/messages"
    assert seen["x_api_key"] == key and seen["authorization"] is None


# ============================================================ cost of the probe itself

def test_the_probe_asks_for_the_smallest_billable_response(stub):
    stub.script = {"m": (200, BODY_OK)}
    probe.run_probe(cfg(["m"]), envfor(stub), retries=0)
    body = stub.seen[0]["body"]
    assert body["max_tokens"] == probe.PROBE_MAX_TOKENS == 1
    assert body["messages"] == [{"role": "user", "content": "1"}]


def test_one_request_per_model_and_no_more(stub):
    stub.script = {"a": (200, BODY_OK), "b": (200, BODY_OK), "c": (200, BODY_OK)}
    probe.run_probe(cfg(["a", "b", "c"]), envfor(stub), retries=2)
    assert len(stub.seen) == 3
    assert sorted(stub.hits.values()) == [1, 1, 1]


def test_dry_run_sends_absolutely_nothing(stub):
    """How this module was developed: the plan is inspectable without a single request."""
    stub.script = {"m": (200, BODY_OK)}
    report = probe.run_probe(cfg(["m"]), envfor(stub), dry_run=True)
    assert stub.seen == []
    assert report.probes[0].verdict == NOT_PROBED
    assert "nothing was sent" in report.probes[0].note
    assert "STUB_KEY" in report.probes[0].note  # the NAME, not the value
    assert INVALID_KEY not in report.probes[0].note


# ============================================================ configuration

def test_an_unset_credential_variable_is_reported_not_silently_skipped():
    """"You did not configure this" and "this is broken" need different fixes, and a probe
    that reports only what it reached reports the wrong thing."""
    report = probe.run_probe(cfg(["m"]), {"STUB_BASE": "http://127.0.0.1:1"}, retries=0)
    p = report.probes[0]
    assert p.verdict == NO_CREDENTIAL and "STUB_KEY" in p.note
    assert p.fatal


def test_an_unset_base_url_is_reported_the_same_way():
    report = probe.run_probe(cfg(["m"]), {"STUB_KEY": INVALID_KEY}, retries=0)
    assert report.probes[0].verdict == NO_CREDENTIAL
    assert "STUB_BASE" in report.probes[0].note


@pytest.mark.parametrize("bad,fragment", [
    ({"providers": [{"id": "p", "wire": "carrier-pigeon", "base_url_env": "A",
                     "api_key_env": "B", "models": ["m"]}]}, "wire"),
    ({"providers": [{"id": "p", "wire": "openai", "models": ["m"]}]}, "required"),
    ({"providers": [{"id": "p", "wire": "openai", "base_url_env": "A",
                     "api_key_env": "B", "models": []}]}, "non-empty"),
    ({"providers": ["not an object"]}, "not an object"),
])
def test_misconfiguration_is_reported_per_entry(bad, fragment):
    report = probe.run_probe(bad, {"A": "http://x", "B": "k"}, retries=0)
    assert report.probes[0].verdict == MISCONFIGURED
    assert fragment in report.probes[0].note


def test_a_config_without_a_providers_list_is_a_single_clear_failure():
    report = probe.run_probe({}, {}, retries=0)
    assert report.probes[0].verdict == MISCONFIGURED
    assert not report.ok


def test_no_provider_endpoint_or_model_name_is_hardcoded_in_the_module():
    """The target list is operator configuration kept outside this repository. A probe
    that shipped a provider list would both go stale and disclose the contestant set."""
    import inspect
    source = inspect.getsource(probe)
    for marker in ("http://", "https://"):
        for line in source.splitlines():
            if marker in line and "127.0.0.1" not in line:
                assert line.lstrip().startswith(("#", "*", '"', "'")) or '"""' in source, \
                    f"module contains a live URL: {line.strip()}"


# ============================================================ report + exit codes

def test_the_report_separates_the_three_questions_per_model(stub):
    stub.script = {"good": (200, BODY_OK), "broke": (402, BODY_INSUFFICIENT_BALANCE),
                   "nope": (401, '{"message":"Invalid API key"}')}
    report = probe.run_probe(cfg(["good", "broke", "nope"]), envfor(stub), retries=0)
    assert verdicts(report) == {"stub/good": OK, "stub/broke": NO_BALANCE,
                                "stub/nope": AUTH_FAILED}
    text = report.render()
    assert "PROBE FAILED" in text
    assert "reach" in text and "auth" in text and "balance" in text
    assert "not a model result" in text


def test_a_healthy_set_renders_as_passed(stub):
    stub.script = {"a": (200, BODY_OK), "b": (200, BODY_OK)}
    report = probe.run_probe(cfg(["a", "b"]), envfor(stub), retries=0)
    assert "PROBE PASSED" in report.render() and report.ok


def test_cli_exits_two_when_there_is_no_provider_config(tmp_path, capsys):
    rc = probe.main(["--providers", str(tmp_path / "absent.json")])
    assert rc == 2
    err = capsys.readouterr().err
    assert "no provider config" in err and "providers" in err


def test_cli_exits_two_on_unparseable_config(tmp_path, capsys):
    bad = tmp_path / "providers.json"
    bad.write_text("{not json", encoding="utf-8")
    assert probe.main(["--providers", str(bad)]) == 2


def test_cli_exits_one_when_a_contestant_cannot_serve(stub, tmp_path, monkeypatch, capsys):
    stub.script = {"broke": (402, BODY_INSUFFICIENT_BALANCE)}
    conf = tmp_path / "providers.json"
    conf.write_text(json.dumps(cfg(["broke"])), encoding="utf-8")
    monkeypatch.setenv("STUB_BASE", stub.base_url)
    monkeypatch.setenv("STUB_KEY", INVALID_KEY)
    assert probe.main(["--providers", str(conf), "--retries", "0"]) == 1
    assert INVALID_KEY not in capsys.readouterr().out


def test_cli_exits_zero_when_everything_is_fundable(stub, tmp_path, monkeypatch):
    stub.script = {"good": (200, BODY_OK)}
    conf = tmp_path / "providers.json"
    conf.write_text(json.dumps(cfg(["good"])), encoding="utf-8")
    monkeypatch.setenv("STUB_BASE", stub.base_url)
    monkeypatch.setenv("STUB_KEY", INVALID_KEY)
    assert probe.main(["--providers", str(conf), "--retries", "0"]) == 0


def test_cli_dry_run_contacts_nothing(stub, tmp_path, monkeypatch):
    conf = tmp_path / "providers.json"
    conf.write_text(json.dumps(cfg(["m"])), encoding="utf-8")
    monkeypatch.setenv("STUB_BASE", stub.base_url)
    monkeypatch.setenv("STUB_KEY", INVALID_KEY)
    assert probe.main(["--providers", str(conf), "--dry-run"]) == 0
    assert stub.seen == []


def test_the_probe_config_is_resolved_beside_the_credential_file_never_inside_the_repo():
    from pathlib import Path
    p = probe.resolve_providers_file({"HOME": "/h"})
    assert p == Path("/h/.config/dmaic/providers.json")
    assert probe.resolve_providers_file({"DMAIC_PROVIDERS_FILE": "/x/p.json"}) == Path("/x/p.json")
