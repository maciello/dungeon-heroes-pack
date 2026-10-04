#!/bin/bash
# Server startup: update the pack, then start Minecraft.
# Usage: bash start.sh <pack.toml URL>    Env: SERVER_MEMORY (MiB, default 8192), SERVER_JARFILE (default fabric-server.jar)
set -e
java -jar packwiz-installer-bootstrap.jar -g -s server "$1"
exec java -Xms128M -Xmx"${SERVER_MEMORY:-8192}"M -jar "${SERVER_JARFILE:-fabric-server.jar}" nogui
