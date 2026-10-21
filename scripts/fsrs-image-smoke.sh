#!/bin/sh
# Build the production image and prove Smart Review schedules inside it.
# Does not deploy and does not touch a protected database.
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
