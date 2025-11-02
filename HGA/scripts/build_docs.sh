#!/bin/bash

# ==============================================================================
# HGA Documentation Build Script
#
# This script builds the project documentation using MkDocs.
#
# Usage:
#   chmod +x scripts/build_docs.sh
#   ./scripts/build_docs.sh        # To build the static site
#   ./scripts/build_docs.sh serve  # To build and serve locally for preview
# ==============================================================================

set -e

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "Error: mkdocs is not installed."
    echo "Please install it with: pip install mkdocs mkdocs-material mkdocstrings[python]"
    exit 1
fi

ACTION=${1:-build}

echo "--- Building HGA Documentation ---"

if [ "$ACTION" == "serve" ]; then
    echo "Starting local documentation server..."
    echo "Docs will be available at http://127.0.0.1:8000"
    echo "Press Ctrl+C to stop the server."
    mkdocs serve
else
    echo "Building static documentation site..."
    mkdocs build
    echo ""
    echo "--- Build Complete ---"
    echo "The static site has been generated in the 'site/' directory."
    echo "You can open 'site/index.html' in your browser to view it."
fi