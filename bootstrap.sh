#!/usr/bin/env bash

set -e
set -u
set -o pipefail

if [[ $EUID -ne 0 ]]; then
	echo "Please run as root"
	exit 1
fi

apt-get update
apt-get install -y curl

curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh

cd "$(dirname "$0")"
/root/.local/bin/uv run main.py
