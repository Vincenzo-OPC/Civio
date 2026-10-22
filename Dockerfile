# Node 22 stays in the runtime image so Smart Review can run ts-fsrs.
# npm and the frontend node_modules are removed after the asset build.
FROM node:22.23.2-bookworm-slim AS nodebin

# Pinned to a patched PHP (CVE-2026-109618 / CVE-2026-109619, fixed in 8.4.27).
# The digest was checked against the registry: its PHP_VERSION is 8.4.27.
# Override only for tests; the guard below rejects a vulnerable base.
ARG PHP_BASE_IMAGE=serversideup/php:8.4.27-fpm-nginx-v4.5.3@sha256:f6768762e0511e2b710294eac0949361c17ccbca25016a5a908f3df3e933a512
FROM ${PHP_BASE_IMAGE}

WORKDIR /var/www/html

USER root

# Build fails here when the base image runs a vulnerable PHP.
COPY scripts/security/assert-patched-php.php scripts/security/patched-php-minimums.php /tmp/php-guard/
RUN php /tmp/php-guard/assert-patched-php.php && rm -rf /tmp/php-guard

COPY --from=nodebin /usr/local/bin/node /usr/local/bin/node
COPY --from=nodebin /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -sf ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -sf ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx \
    && install-php-extensions pdo_pgsql pdo_sqlite gd zip bcmath opcache sodium \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=www-data:www-data . .

ENV APP_NAME="Civio"

# A disposable key lets Composer and Wayfinder boot. It is not the runtime key.
RUN export APP_KEY="base64:$(php -r 'echo base64_encode(random_bytes(32));')" \
    && composer install --no-dev --optimize-autoloader

# Same kind of disposable key. The entrypoint does not reuse it.
RUN export APP_KEY="base64:$(php -r 'echo base64_encode(random_bytes(32));')" \
    && npm ci && npm run build \
    && mkdir -p /tmp/fsrs-keep \
    && cp -a node_modules/ts-fsrs /tmp/fsrs-keep/ts-fsrs \
    && rm -rf node_modules /root/.npm \
    && mkdir -p node_modules \
    && mv /tmp/fsrs-keep/ts-fsrs node_modules/ts-fsrs \
    && rm -rf /usr/local/lib/node_modules /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack \
    && chown -R www-data:www-data node_modules

COPY --chmod=755 scripts/00-laravel-deploy.sh /etc/entrypoint.d/00-laravel-deploy.sh

EXPOSE 8080

RUN mkdir -p storage/logs bootstrap/cache \
    && chown -R www-data:www-data storage bootstrap/cache \
    && chmod -R u+rwX storage bootstrap/cache

USER www-data
