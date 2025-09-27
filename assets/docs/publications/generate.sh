#!/bin/bash
# Wrapper script to run the secure publication generation from this directory
# The actual scripts are now in .github/config for security

# Get the absolute path to this script's directory
PUBLICATIONS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_DIR="$PUBLICATIONS_DIR/../../../.github/config"

echo "🔧 Running secure publication generation..."
echo "📁 Publications directory: $PUBLICATIONS_DIR"
echo "🔒 Scripts location: $SCRIPT_DIR"
echo ""

# Run the secure script
bash "$SCRIPT_DIR/genPubHTML.sh" "$1"

echo ""
echo "✅ Publication generation complete!"
echo "📄 Generated files are in: $PUBLICATIONS_DIR"