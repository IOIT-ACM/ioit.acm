#!/bin/bash

# This script is designed to prepare files for deployment by copying the necessary content to a
# specified destination directory, running a Perl script to minify JavaScript and CSS files,
# and then cleaning up temporary files. It performs the following steps:
#
# 1. It checks if the destination directory (`DEST_DIR`) exists. If it does, the script deletes
#    it to ensure a fresh copy of the files is created.
# 2. It copies the content of the current directory to the destination directory using `rsync`,
#    excluding specific files and directories (such as `.git`, `node_modules`, and Python bytecode).
# 3. After the copy is complete, the script checks for the presence of a Perl script (`minify.pl`)
#    in the destination directory and runs it to minify the JavaScript and CSS files.
# 4. Once the Perl script has run successfully, the script deletes the `minify.pl` and
#    `web-minifier.config.json` files, as they are no longer needed and then it compresses the app dir.
# 5. Finally, the script ensures that after all operations are complete, it returns to the original
#    directory where it was invoked.
#
# This process ensures that only the necessary files are copied and that the generated minified
# files can be safely transferred to a cPanel server for deployment.

DEST_DIR=~/Downloads/ioit.acm.org

EXCLUDE_LIST=(
	".git"
	"*__pycache__"
	"*pycache"
	"node_modules"
	"package-lock.json"
	".venv"
	".gitignore"
	"*.DS_Store"
	"README.md"
	"docs"
	"*.pyc"
	"tailwind.config.js"
	"run.py"
	"README.md"
	".gitignore"
	"build.sh"
	"package.json"
	"requirements.txt"
	".env"
	".env.example"
	"Dockerfile"
	"tests"
)

error_exit() {
	echo "Error: $1" >&2
	exit 1
}

if [ -d "$DEST_DIR" ]; then
	echo "Destination directory $DEST_DIR already exists. Deleting it..."
	rm -rf "$DEST_DIR" || error_exit "Failed to delete existing destination directory"
fi

mkdir -p "$DEST_DIR" || error_exit "Could not create destination directory"

EXCLUDE_PARAMS=()
for EXCLUDE_ITEM in "${EXCLUDE_LIST[@]}"; do
	EXCLUDE_PARAMS+=("--exclude=$EXCLUDE_ITEM")
done

echo "Starting file copy..."
rsync -a --delete "${EXCLUDE_PARAMS[@]}" ./ "$DEST_DIR/" || error_exit "File copy failed"

echo "Successfully copied contents to $DEST_DIR"

if [ -f "$DEST_DIR/minifier/minify.pl" ]; then
	echo "Running Perl script in $DEST_DIR..."
	CURRENT_DIR=$(pwd)
	cd "$DEST_DIR" || error_exit "Failed to change directory to $DEST_DIR"

	perl ./minifier/minify.pl || {
		cd "$CURRENT_DIR" || exit 1
		error_exit "Perl script execution failed"
	}

	echo "Cleaning up files..."
	rm -f minify.pl web-minifier.config.json || {
		cd "$CURRENT_DIR" || exit 1
		error_exit "Failed to delete files"
	}

	zip -r "app.zip" "app" || error_exit "Failed to compress app directory"

	echo "Deleting app directory..."
	rm -rf "app" || error_exit "Failed to delete app directory"
	rm -rf "minifier" || error_exit "Failed to delete minifier directory"

	echo "App directory compressed and deleted successfully."

	cd "$CURRENT_DIR" || exit 1
else
	error_exit "Perl script $DEST_DIR/minify.pl not found"
fi

echo "Script completed successfully."
