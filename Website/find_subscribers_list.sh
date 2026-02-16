#!/bin/bash
# Script to find and display the subscribers list file

echo "="*70
echo "FINDING SUBSCRIBER LIST FILE"
echo "="*70

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBSCRIBERS_FILE="$SCRIPT_DIR/subscribers_list.txt"

echo ""
echo "Looking for subscribers_list.txt..."
echo ""

if [ -f "$SUBSCRIBERS_FILE" ]; then
    echo "✓ FILE FOUND!"
    echo ""
    echo "Location: $SUBSCRIBERS_FILE"
    echo "Size: $(ls -lh "$SUBSCRIBERS_FILE" | awk '{print $5}')"
    echo "Last modified: $(ls -l "$SUBSCRIBERS_FILE" | awk '{print $6, $7, $8}')"
    echo ""
    echo "="*70
    echo "FILE CONTENTS:"
    echo "="*70
    cat "$SUBSCRIBERS_FILE"
else
    echo "✗ FILE NOT FOUND at: $SUBSCRIBERS_FILE"
    echo ""
    echo "The file will be created automatically when:"
    echo "1. A user subscribes via the website"
    echo "2. Or you run: cd backend && python test_export.py"
    echo ""
    echo "Current directory: $SCRIPT_DIR"
    echo "Files in this directory:"
    ls -la "$SCRIPT_DIR" | grep -E "subscribers|\.txt|\.csv" || echo "  (no subscriber files found)"
fi

echo ""
echo "="*70









