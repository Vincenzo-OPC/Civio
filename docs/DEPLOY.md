# Civio hosting decision - pending GT

Hosting is **undecided**. Earlier Cloud Run/Neon/Cloudflare and Koyeb/Neon/Netlify proposals conflict; neither is an approved deployment target. Select hosting with GT before creating accounts, enabling billing or preparing a release.

No deployment, paid service or Netlify credit spending is authorized. Preserve all Netlify ignore/build-skip settings. Every new commit includes [skip netlify]. A code push is not permission to publish.

## MSI runtime boundaries

- Canonical source: C:\Users\GT\Desktop\Claude\Civio, branch main.
- Civio live study: civio-local-app at localhost:8090; civio-local-db on localhost:5434.
- Hermes: 8642.
- Never stop, restart, rebuild, query or modify these services for development. Never use student data for tests.

The task-owned security test container is civio-security-check-20261020. It has no network or published ports, uses an isolated task checkout and its own dependency volumes, and runs PHPUnit with SQLite in memory. Existing review checkouts and their dependency volumes remain preserved.

Keep .env, databases, credentials and preview overrides uncommitted. AI credentials stay server-side; never place them in VITE variables.
