# Entire.io on this repo

Entire follows the GitHub repo, not the Windows folder name.

- GitHub: `Vincenzo-OPC/Civio`
- Web: https://entire.io (sign in Vincenzo-OPC, open Civio)
- Checkpoints: git-refs strategy (`refs/entire/checkpoints/...`)
- Canonical MSI study app: Docker `hiraya-review-app` on `localhost:8080` (do not break; never touch Hermes `:8642`)
- Box build tree: `/workspace/civio-build` (agents). Do not reuse `/workspace/civio-audit`.

## Enable (once per clone)

```bash
# Linux / box
curl -fsSL https://entire.io/install.sh | bash
cd /path/to/Civio
entire enable --agent cursor --project --telemetry=false --absolute-git-hook-path
entire status
```

```powershell
# GT MSI
irm https://entire.io/install.ps1 | iex
cd C:\Users\GT\Desktop\Grok\CSE\Hiraya-Review   # or the Civio clone path
entire enable --agent cursor --project --telemetry=false --absolute-git-hook-path
entire status
```

Committed: `.entire/settings.json`, `.entire/.gitignore`, `.entire/README.md`, `.cursor/hooks.json`.
Never commit `.entire/metadata/`, logs, or `settings.local.json`.

## Notes

- Telemetry off in this repo.
- Redaction rules cover common API key / PAT shapes (best-effort).
- If `entire enable` cannot run in a headless cloud session, commit the settings
  files (already done) and run enable on the MSI so local git hooks install.
