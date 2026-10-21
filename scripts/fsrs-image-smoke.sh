#!/bin/sh
# Build the production image and prove Smart Review schedules inside it.
# Does not deploy and does not touch a protected database.
#
# This sandbox maps only uid 0, so dockerd fails with
# "failed to register layer: lchown ... invalid argument"
# before the image exists. Do not treat that as a passed build.
# Run this script on a Docker host that can unpack image layers.
set -eu
cd "$(dirname "$0")/.."
IMAGE="${CIVIO_SMOKE_IMAGE:-civio-fsrs-smoke}"
docker build -t "$IMAGE" .
APP_KEY="$(php artisan key:generate --show)"
docker run --rm \
    -e APP_KEY="$APP_KEY" \
    --entrypoint php \
    "$IMAGE" \
    scripts/fsrs-image-smoke.php
