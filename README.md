# ai_base_doc

Base AI agent instructions — used as a Git submodule at `.agents/`.

**Full documentation:** [github.com/n0kzy/ai_base_doc](https://github.com/n0kzy/ai_base_doc)

## Quick Start

```bash
# Add to a project
git clone https://github.com/n0kzy/ai_base_doc.git .agents

# Upgrade
cd .agents && git pull origin main && cd ..

# Clone with submodules
git clone --recurse-submodules <repo-url>
```

## Skills

- Catalog: [skills/SOURCES.md](skills/SOURCES.md)
- Local: Python, Vercel React, code duplication scan
- Third-party skills sit directly under `skills/<name>/` (no `vendor/`). Refresh:

```powershell
powershell -File .agents/scripts/vendor-external-skills.ps1
```

Upstream list: [skills/SOURCES.md](skills/SOURCES.md).

Wire into app repos: copy [docs/bootstrap-agents.mdc](docs/bootstrap-agents.mdc) to `.cursor/rules/agents.mdc`.
``` 
