#!/bin/bash
set -e

tag=$(gh release list --repo rajtarn/spytify --exclude-drafts --exclude-pre-releases --json tagName --jq '.[0].tagName')

echo "Building release assets from tag: $tag..."

SPYTIFY_VERSION=$tag python3 -m build
