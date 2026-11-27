#!/usr/bin/env bash
# Starts the account's Redis (used for rate limit storage) if it is not
# answering, and logs every start so restarts can be tracked.
#
# Run from cron every 5 minutes, which also covers server reboots:
#   */5 * * * * bash $HOME/ioit.acm/deploy/redis-keepalive.sh
#
# Redis listens on a private unix socket only (no TCP port), keeps nothing on
# disk and is capped at 32MB. Point the app at it with:
#   RATELIMIT_STORAGE_URI=redis+unix://$HOME/redis/redis.sock

set -euo pipefail

REDIS_BIN="${REDIS_BIN:-/opt/alt/redis/bin}"
REDIS_DIR="${REDIS_DIR:-$HOME/redis}"
SOCKET="$REDIS_DIR/redis.sock"
LOG="$REDIS_DIR/keepalive.log"

mkdir -p "$REDIS_DIR"
chmod 700 "$REDIS_DIR"

if "$REDIS_BIN/redis-cli" -s "$SOCKET" ping >/dev/null 2>&1; then
	exit 0
fi

echo "$(date '+%F %T') redis not responding, starting it" >>"$LOG"

"$REDIS_BIN/redis-server" \
	--port 0 \
	--unixsocket "$SOCKET" \
	--unixsocketperm 700 \
	--daemonize yes \
	--pidfile "$REDIS_DIR/redis.pid" \
	--logfile "$REDIS_DIR/redis.log" \
	--dir "$REDIS_DIR" \
	--save "" \
	--appendonly no \
	--maxmemory 32mb \
	--maxmemory-policy volatile-ttl

for _ in 1 2 3 4 5; do
	if "$REDIS_BIN/redis-cli" -s "$SOCKET" ping >/dev/null 2>&1; then
		echo "$(date '+%F %T') redis started" >>"$LOG"
		exit 0
	fi
	sleep 1
done

echo "$(date '+%F %T') redis failed to start, see $REDIS_DIR/redis.log" >>"$LOG"
exit 1
