#!/usr/bin/env bash
#
# Campaign preflight -- standalone.
#
#     harbor/scripts/preflight.sh [--no-pull] [--jobs-dir DIR] [--json] ...
#
# Exit 0 = the host can run a campaign. Exit 1 = at least one hard failure, each printed
# with the command that fixes it. Nothing is launched either way.
#
# This is a thin wrapper. The checks live in `dmaic_harbor.preflight` so that the
# supervisor can call the same code in-process -- a preflight that only exists as a shell
# script is a preflight that the thing actually launching the campaign will not run.
#
# Run it on its own before a sweep, or let `launch-campaign.sh` run it for you.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
harbor_root="$(dirname "$here")"

# Prefer an installed `dmaic-harbor`; fall back to the source tree so this works in a
# fresh checkout with nothing installed.
if command -v dmaic-harbor-preflight >/dev/null 2>&1; then
    exec dmaic-harbor-preflight "$@"
fi
exec env PYTHONPATH="$harbor_root/src${PYTHONPATH:+:$PYTHONPATH}" \
    python3 -m dmaic_harbor.preflight "$@"
