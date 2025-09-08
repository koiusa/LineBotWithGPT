#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available
#   https://github.com/vishnubob/wait-for-it

set -e

TIMEOUT=15
HOST="$1"
PORT="$2"
shift 2
CMD="$@"

for i in $(seq $TIMEOUT); do
  nc -z "$HOST" "$PORT" && exec $CMD && exit 0
  sleep 1
done

echo "Timeout waiting for $HOST:$PORT" >&2
exit 1
