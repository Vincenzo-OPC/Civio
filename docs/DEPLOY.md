# Civio deploy plan (not yet executed)

Target free-first stack:

1. **Google Cloud Run** — Laravel Docker image (`Dockerfile`), request-based billing,
   scale to zero, max-instances cap, budget alert.
2. **Neon** — free Postgres; set `DB_CONNECTION=pgsql` and Neon URL in Cloud Run secrets.
3. **Cloudflare** — DNS/CDN for `civio.ph`, Turnstile, Web Analytics; optional AI Gateway.

## Not done yet

- No production Cloud Run service created by Phase 0.
- No Neon project wired from this repo.
- Do not force-push; deploy from `main` after CI green.

## Local Docker (MSI study)

```bash
docker compose up --build
# app :8080, Postgres :5433
```

Never touch Hermes `:8642` or break the MSI `hiraya-review-app` study container.

## Env

Copy `.env.example`. Server-side AI keys only (`OPENAI_API_KEY`, `GEMINI_API_KEY`, …).
Never `VITE_*` secrets. Sentry off unless `SENTRY_LARAVEL_DSN` is set.
