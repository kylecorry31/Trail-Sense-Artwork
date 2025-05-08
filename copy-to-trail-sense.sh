#!/bin/bash

# Exit on any error
set -e

# Step 0: Check for input
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <image_path>"
    exit 1
fi

# Step 1: Copy image to ../Trail-Sense/survival-guide-book/images (with - replaced by _)
INPUT_IMAGE="$1"
BASENAME=$(basename "$INPUT_IMAGE")
NEW_NAME="${BASENAME//-/_}"
DEST_DIR="../Trail-Sense/survival-guide-book/images"
DEST_PATH="$DEST_DIR/$NEW_NAME"

# The dest path relative to the Trail-Sense/scripts folder
RELATIVE_DEST_PATH="../survival-guide-book/images/$NEW_NAME"

mkdir -p "$DEST_DIR"
cp "$INPUT_IMAGE" "$DEST_PATH"

echo "Copied to $DEST_PATH"

# Step 2: Apply filters
python blend-lines.py "$DEST_PATH" "$DEST_PATH" --black-value 50 --white-value 230 --saturation 0.3
echo "Blended lines on $DEST_PATH"

# Use 0.5 on older images, 0.0 on newer images (that use the palette)
python vintage.py "$DEST_PATH" "$DEST_PATH" --sepia 0.0 --noise 5
echo "Applied vintage filter on $DEST_PATH"

# Step 3: Change working dir and convert to webp
pushd ../Trail-Sense/scripts > /dev/null
python convert_to_webp.py "$RELATIVE_DEST_PATH"
echo "Converted to WEBP"

# Step 4: Run replace-image.py
FILENAME_ONLY=$(basename "$DEST_PATH")
python replace-image.py converted.webp "$FILENAME_ONLY"
echo "Replaced image in book for $FILENAME_ONLY"
popd > /dev/null
