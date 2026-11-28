#!/usr/bin/env bash
# Deploys the commit checked out in $REPO_DIR to the CloudLinux Python app in
# $APP_ROOT (served by LiteSpeed lswsgi).
#
# CI checks out the tested commit first and then runs this script:
#   git -C ~/ioit.acm fetch origin && git -C ~/ioit.acm reset --hard <sha>
#   bash ~/ioit.acm/deploy/deploy.sh
#
# The host has a 200 process limit that also counts threads, so every tool
# here runs with capped concurrency.

set -euo pipefail

REPO_DIR="${REPO_DIR:-$HOME/ioit.acm}"
# The app folder is named after its Python version: LiteSpeed caches each
# app's Python home by folder, so a Python upgrade needs a new app folder
# (see README, "Upgrading Python").
APP_ROOT="${APP_ROOT:-$HOME/website-312}"
VENV="${VENV:-$HOME/virtualenv/website-312/3.12}"
UV="${UV:-$HOME/.local/bin/uv}"
HEALTH_URL="${HEALTH_URL:-https://ioit.acm.org/}"
PREVIOUS_DIR="${PREVIOUS_DIR:-$HOME/releases/website/previous}"
LOCK_FILE="$HOME/.deploy-website.lock"

# uv: cap parallel downloads, installs and builds; never download Python.
export UV_CONCURRENT_DOWNLOADS=4
export UV_CONCURRENT_INSTALLS=2
export UV_CONCURRENT_BUILDS=1
export UV_PYTHON_DOWNLOADS=never
export UV_NO_PROGRESS=1

step() { printf '\n>>> %s\n' "$1"; }
fail() {
	echo "Error: $1" >&2
	exit 1
}

exec 9>"$LOCK_FILE"
flock -n 9 || fail "another deploy is already running"

cd "$REPO_DIR"
COMMIT="$(git rev-parse --short HEAD)"
step "Deploying $COMMIT"

[ -x "$VENV/bin/python" ] || fail "Python environment not found at $VENV"
[ -x "$UV" ] || fail "uv not found at $UV"

step "Installing Python dependencies"
LOCK_HASH="$(sha256sum uv.lock | cut -d' ' -f1)"
LOCK_STAMP="$VENV/.deployed-uv-lock"
if [ "$(cat "$LOCK_STAMP" 2>/dev/null)" != "$LOCK_HASH" ]; then
	REQUIREMENTS="$(mktemp)"
	trap 'rm -f "$REQUIREMENTS"' EXIT
	"$UV" export --frozen --no-dev --no-emit-project --format requirements.txt \
		--output-file "$REQUIREMENTS" >/dev/null
	"$UV" pip install --python "$VENV/bin/python" --requirement "$REQUIREMENTS"
	echo "$LOCK_HASH" >"$LOCK_STAMP"
else
	echo "uv.lock unchanged, skipping."
fi

step "Building frontend libraries"
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
# nvm does not support `set -u`.
set +u
# shellcheck source=/dev/null
. "$NVM_DIR/nvm.sh"
nvm use --silent >/dev/null || fail "Node $(cat .nvmrc) is not installed, run: nvm install $(cat .nvmrc)"
set -u
NPM_HASH="$(sha256sum package-lock.json | cut -d' ' -f1)"
NPM_STAMP="node_modules/.deployed-package-lock"
if [ "$(cat "$NPM_STAMP" 2>/dev/null)" != "$NPM_HASH" ]; then
	UV_THREADPOOL_SIZE=2 npm ci --omit=dev --no-audit --no-fund
	echo "$NPM_HASH" >"$NPM_STAMP"
else
	echo "package-lock.json unchanged, skipping npm ci."
fi
npm run --silent vendor

step "Saving current release for rollback"
mkdir -p "$PREVIOUS_DIR"
if [ -d "$APP_ROOT/app" ]; then
	rsync -a --delete --exclude=/static/uploads/ "$APP_ROOT/app/" "$PREVIOUS_DIR/app/"
	cp -p "$APP_ROOT/wsgi.py" "$APP_ROOT/passenger_wsgi.py" "$PREVIOUS_DIR/" 2>/dev/null || true
fi

publish() {
	# $1: source dir holding app/, wsgi.py and passenger_wsgi.py
	# static/uploads/ holds files uploaded through the admin pages, so it is
	# never copied over or deleted.
	rsync -a --delete \
		--exclude=__pycache__/ --exclude='*.pyc' \
		--exclude=/static/uploads/ \
		"$1/app/" "$APP_ROOT/app/"
	cp -p "$1/wsgi.py" "$1/passenger_wsgi.py" "$APP_ROOT/"
	mkdir -p "$APP_ROOT/app/static/uploads/notify" "$APP_ROOT/app/static/uploads/events" "$APP_ROOT/tmp"
	touch "$APP_ROOT/tmp/restart.txt"
}

healthy() {
	local code
	for _ in $(seq 1 10); do
		code="$(curl -s -o /dev/null --max-time 10 -w '%{http_code}' "$HEALTH_URL" || true)"
		if [ "$code" = "200" ]; then
			echo "$HEALTH_URL returned 200"
			return 0
		fi
		echo "$HEALTH_URL returned $code, retrying..."
		sleep 3
	done
	return 1
}

step "Publishing to $APP_ROOT"
publish "$REPO_DIR"

step "Checking the site"
if healthy; then
	echo "Deployed $COMMIT."
	exit 0
fi

step "Health check failed, rolling back"
if [ -d "$PREVIOUS_DIR/app" ]; then
	publish "$PREVIOUS_DIR"
	healthy || echo "Site is still unhealthy after rollback, check $APP_ROOT/stderr.log" >&2
else
	echo "No previous release to roll back to." >&2
fi
fail "deploy of $COMMIT failed health check"
