#!/usr/bin/env bash
# Export the credentials the AGENT needs for one provider, derived from providers.json.
#
#     source scripts/campaign-env.sh
#     source scripts/agent-env.sh zai          # then: harbor run -c job.yaml
#
# Why this exists. `providers.json` tells the PROBE how to reach each provider —
# `base_url_env`, `api_key_env`, and the wire protocol. It tells the agent nothing. The agent
# is litellm inside the harness and reads the conventional per-wire variables
# (ANTHROPIC_API_KEY / ANTHROPIC_BASE_URL, OPENAI_API_KEY / OPENAI_BASE_URL), which are NOT the
# variables the credential file defines: a GLM model served over the Anthropic wire lives in
# ZAI_KEY and ZAI_BASE.
#
# Nothing bridged the two. The probe would report `zai/glm-5.3-flash ok` and the campaign would
# then authenticate as whatever happened to be in ANTHROPIC_API_KEY — a different provider, or
# nothing. That is the failure the probe exists to prevent, arriving through the one gap the
# probe cannot see, and it is recorded as trials the model failed.
set -u

_provider="${1:-}"
if [ -z "$_provider" ]; then
    echo "usage: source scripts/agent-env.sh <provider-id>   (ids: $(
        python3 - <<'PY'
import json, os, pathlib
p = pathlib.Path(os.environ.get("DMAIC_PROVIDERS_FILE",
                                pathlib.Path.home() / ".config/dmaic/providers.json"))
print(" ".join(e["id"] for e in json.loads(p.read_text())["providers"]))
PY
    ))" >&2
    return 1 2>/dev/null || exit 1
fi

_exports="$(python3 - "$_provider" <<'PY'
import json, os, pathlib, sys

provider_id = sys.argv[1]
path = pathlib.Path(os.environ.get("DMAIC_PROVIDERS_FILE",
                                   pathlib.Path.home() / ".config/dmaic/providers.json"))
entries = json.loads(path.read_text())["providers"]
entry = next((e for e in entries if e["id"] == provider_id), None)
if entry is None:
    sys.exit(f"unknown provider {provider_id!r}; known: "
             + ", ".join(e['id'] for e in entries))

base = os.environ.get(entry["base_url_env"], "").strip()
key = os.environ.get(entry["api_key_env"], "").strip()
missing = [n for n, v in ((entry["base_url_env"], base), (entry["api_key_env"], key)) if not v]
if missing:
    sys.exit(f"{provider_id}: {', '.join(missing)} not set — source scripts/campaign-env.sh first")

# The variables litellm reads for each wire. The model_name prefix in the job config must match
# the wire: an `anthropic/` model reads the ANTHROPIC_* pair whatever provider actually serves it.
wire = entry.get("wire", "openai")
pairs = {"anthropic": (("ANTHROPIC_API_KEY", key), ("ANTHROPIC_BASE_URL", base),
                       ("ANTHROPIC_API_BASE", base)),
         "openai": (("OPENAI_API_KEY", key), ("OPENAI_BASE_URL", base),
                    ("OPENAI_API_BASE", base))}.get(wire)
if pairs is None:
    sys.exit(f"{provider_id}: unsupported wire {wire!r}")

for name, value in pairs:
    print(f"export {name}={value!r}")
print(f"export DMAIC_AGENT_PROVIDER={provider_id!r}")
print(f"export DMAIC_AGENT_WIRE={wire!r}", file=sys.stderr)
PY
)" || { echo "agent-env: $_exports" >&2; unset _provider _exports; return 1 2>/dev/null || exit 1; }

eval "$_exports"
echo "agent-env: $_provider ($(python3 -c "
import json,os,pathlib,sys
p=pathlib.Path(os.environ.get('DMAIC_PROVIDERS_FILE', pathlib.Path.home()/'.config/dmaic/providers.json'))
e=next(x for x in json.loads(p.read_text())['providers'] if x['id']==sys.argv[1])
print(e.get('wire','openai') + ' wire, models: ' + ', '.join(e['models']))
" "$_provider")) -> agent credentials exported" >&2
unset _provider _exports
