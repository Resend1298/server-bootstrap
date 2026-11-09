#!/usr/bin/env zsh

set -e
set -u
set -o pipefail

if [[ $EUID -ne 0 ]]; then
	echo "Please run as root"
	exit 1
fi

UV_NO_MODIFY_PATH=1 /root/.local/bin/uv self update

cd "$(dirname "$0")"
/root/.local/bin/uv run main.py
