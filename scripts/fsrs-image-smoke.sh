#!/bin/sh
# Build the production image and prove Smart Review schedules inside it.
# Does not deploy, push the image, publish a port, or touch a protected database.
#
# This sandbox maps only uid 0, so dockerd fails with
# "failed to register layer: lchown ... invalid argument"
# before the image exists. Do not treat that as a passed build.
# A normal Docker host, including a GitHub-hosted Ubuntu runner, can run it.
set -eu
cd "$(dirname "$0")/.."
IMAGE="${CIVIO_SMOKE_IMAGE:-civio-fsrs-smoke}"

# A clean runner has no Composer install, so `php artisan key:generate`
# cannot boot. The key is disposable and is passed only to this container.
if ! command -v openssl >/dev/null 2>&1; then
    echo "openssl is required to create a disposable APP_KEY." >&2
    exit 1
fi
APP_KEY="base64:$(openssl rand -base64 32 | tr -d '\n')"

docker build -t "$IMAGE" .
docker run --rm \
    -e APP_KEY="$APP_KEY" \
    --entrypoint php \
    "$IMAGE" \
    scripts/fsrs-image-smoke.php
