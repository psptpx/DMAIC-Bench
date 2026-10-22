#!/usr/bin/env bash
# Source the campaign credentials from outside the repository, and refuse to run without them.
#
#     source scripts/campaign-env.sh && harbor run -c job.yaml
#
# Resolution order: $DMAIC_ENV_FILE, then ~/.config/dmaic/campaign.env. Nothing in the
# repository is ever read, so a credential cannot be picked up from a checkout by accident.
set -u
_env_file="${DMAIC_ENV_FILE:-$HOME/.config/dmaic/campaign.env}"

if [ ! -f "$_env_file" ]; then
    echo "no credential file at $_env_file" >&2
    echo "copy .env.example there, chmod 600, and fill it in (see the header in that file)" >&2
    return 1 2>/dev/null || exit 1
fi

# A world- or group-readable bearer token is a finding, not a warning.
_mode="$(stat -f '%A' "$_env_file" 2>/dev/null || stat -c '%a' "$_env_file" 2>/dev/null)"
case "$_mode" in
    600|400) ;;
    *) echo "refusing to source $_env_file: mode $_mode; run: chmod 600 $_env_file" >&2
       return 1 2>/dev/null || exit 1 ;;
esac

set -a
# shellcheck disable=SC1090
. "$_env_file"
set +a
unset _env_file _mode
