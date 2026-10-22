"""``steward`` — the agent-facing CLI wrapper around the data steward HTTP service.

Installed at ``spec.STEWARD_CLI`` (/usr/local/bin/steward) in the agent image. The steward
is the agent's ONLY channel to project data; there is no other copy of the data in the
container and there is no network beyond loopback.

    steward request "the gage repeatability study"   # free
    steward declare grr_pct 18.4                     # free
    steward declare stable false                     # free
    steward provision "what is the drawing tolerance" # METERED as an autonomy turn
    steward status                                   # free

``--json`` prints the raw service response instead of the human message. Exit status is 0
whenever the service answered (a refusal is an answer, and the agent is expected to read
it and adapt); 2 means the service could not be reached or the request was malformed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

try:
    from dmaic_harbor import spec
except ImportError:  # pragma: no cover
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from dmaic_harbor import spec

ENV_BASE = "DMAIC_STEWARD_BASE"
TIMEOUT = 30.0


def base_url() -> str:
    return os.environ.get(ENV_BASE, spec.STEWARD_BASE).rstrip("/")


#: The steward is loopback-only and the container has no network. Container runtimes
#: (podman among them) inject HTTP_PROXY/HTTPS_PROXY pointing at a host-side proxy, and
#: urllib would then try to resolve that proxy's hostname and fail with a name-resolution
#: error that looks like "the steward is down". Talk to the steward with proxies disabled.
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(path: str, payload=None, method: str = "POST", base: str | None = None) -> dict:
    url = f"{(base or base_url())}{path}"
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with _OPENER.open(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _emit(resp: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    else:
        print(resp.get("message", ""))
        if resp.get("refusal"):
            print(f"[refused: {resp['refusal']}]", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="steward",
        description="Ask the project data steward for data, declare results, provision facts.")
    ap.add_argument("--json", action="store_true", help="print the raw JSON response")
    ap.add_argument("--base", default=None, help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="action", required=True)

    p = sub.add_parser("request", help="ask for a batch of project data (free)")
    p.add_argument("text", nargs="+", help="what you need, in plain language")

    p = sub.add_parser("declare", help="record a computed result or conclusion (free)")
    p.add_argument("key")
    p.add_argument("value")

    p = sub.add_parser("provision",
                       help="ask the process owner for a process fact (METERED)")
    p.add_argument("text", nargs="+")

    sub.add_parser("status", help="released / locked / turns used (free)")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.action not in spec.STEWARD_ACTIONS:  # pragma: no cover - argparse guards
        print(f"steward: unknown action {args.action}", file=sys.stderr)
        return 2
    try:
        if args.action == "request":
            resp = call("/request", {"text": " ".join(args.text)}, base=args.base)
        elif args.action == "declare":
            resp = call("/declare", {"key": args.key, "value": args.value}, base=args.base)
        elif args.action == "provision":
            resp = call("/provision", {"text": " ".join(args.text)}, base=args.base)
        else:
            resp = call("/status", method="GET", base=args.base)
    except urllib.error.URLError as exc:
        print(f"steward: cannot reach the steward service at {args.base or base_url()}: "
              f"{exc}", file=sys.stderr)
        return 2
    return _emit(resp, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
