#!/bin/bash
set -e

if [[ -z $1 ]]; then
    tag=$(gh release list --repo rajtarn/spytify --exclude-drafts --exclude-pre-releases --json tagName --jq '.[0].tagName')
else
    tag=$1
fi

echo "Downloading release assets from tag: $tag..."

gh release download $tag --repo rajtarn/spytify --skip-existing --pattern "spytify*.whl"
