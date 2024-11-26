#!/bin/bash

DEST_DIR=~/Downloads/ioit.acm.org

EXCLUDE_LIST=(
	".git"
	"__pycache__"
	"pycache"
	"node_modules"
	"package-lock.json"
	".venv"
	".gitignore"
	".DS_Store"
	"README.md"
	"docs"
)

error_exit() {
	echo "Error: $1" >&2
	exit 1
}

[ -d ./ ] || error_exit "Must be run from a valid directory"

mkdir -p "$DEST_DIR" || error_exit "Could not create destination directory"

# Build the --exclude parameters for rsync
EXCLUDE_PARAMS=()
for EXCLUDE_ITEM in "${EXCLUDE_LIST[@]}"; do
	EXCLUDE_PARAMS+=("--exclude=$EXCLUDE_ITEM")
done

echo "Starting file copy..."
rsync -a --progress "${EXCLUDE_PARAMS[@]}" ./ "$DEST_DIR/" || error_exit "File copy failed"

echo "Successfully copied contents to $DEST_DIR"
