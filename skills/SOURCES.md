# Skills catalog

Upstream attribution only — no per-skill `LICENSE`/`SOURCE` files in folders.

Re-install third-party skills: `powershell -File scripts/vendor-external-skills.ps1`

## Local

| Skill | Folder | Notes |
|-------|--------|--------|
| Python | [python/](python/) | Your rules in `reference.md` |
| Duplication scan | [scan-code-duplication/](scan-code-duplication/) | Local script |
| React / Next.js perf | [vercel-react-best-practices/](vercel-react-best-practices/) | Vercel-style rule bundle |

## Third-party (in `skills/<name>/`)

| Skill folder | Upstream |
|--------------|----------|
| [verification-before-completion](verification-before-completion/) | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| [systematic-debugging](systematic-debugging/) | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) |
| [requesting-code-review](requesting-code-review/) | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/requesting-code-review) |
| [test-driven-development](test-driven-development/) | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) |
| [webapp-testing](webapp-testing/) | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) |
| [pre-deploy-checklist](pre-deploy-checklist/) | [DIBmaster/cursor-skills](https://github.com/DIBmaster/cursor-skills/tree/master/skills/pre-deploy-checklist) |
| [acquire-codebase-knowledge](acquire-codebase-knowledge/) | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/acquire-codebase-knowledge) |
| [refactor-plan](refactor-plan/) | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/refactor-plan) |
| [security-review](security-review/) | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/security-review) |
| [openapi-to-application-code](openapi-to-application-code/) | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/openapi-to-application-code) |
| [postgresql-code-review](postgresql-code-review/) | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/postgresql-code-review) |

## App repo wiring

Copy [../docs/bootstrap-agents.mdc](../docs/bootstrap-agents.mdc) → `.cursor/rules/agents.mdc` in the app.
