# 🧠 ai_base_doc

Base AI agent instructions — designed to be added as a **Git submodule** at `.agents/` in any project.

## Quick Start

### Add to a project
```bash
git submodule add https://github.com/n0kzy/ai_base_doc.git .agents
git commit -m "Add AI agent instructions"
```

### Clone a project that uses it
```bash
git clone --recurse-submodules <your-repo-url>
# or if already cloned:
git submodule update --init --recursive
```

### Upgrade to latest
```bash
cd .agents
git pull origin main
cd ..
git add .agents
git commit -m "Upgrade AI agent instructions"
```

### Remove from a project
```bash
git submodule deinit -f .agents
git rm -f .agents
rm -rf .git/modules/.agents
git commit -m "Remove AI agent instructions"
```

---

## Structure

```
.agents/                  ← this repo, added as submodule
├── coder/
│   └── instructions.md   # Senior SW Engineer role & coding rules
├── shared/
│   └── global_rules.md   # Core protocols (Caveman Protocol, 4-Step Reasoning)
├── skills/
│   ├── data_analysis.py   # Data analysis skill template
│   └── web_scraping.py    # Web scraping skill template
└── README.md              # This file
```

## What's Included

| File | Purpose |
|---|---|
| `shared/global_rules.md` | Universal rules applied to all agents — communication style, reasoning framework |
| `coder/instructions.md` | Role-specific instructions for the coding agent |
| `skills/data_analysis.py` | Reusable data analysis skill |
| `skills/web_scraping.py` | Reusable web scraping skill |

## Project-Specific Overrides

Since `.agents/` is a submodule, you **cannot** add project-specific files into it (they'd be tracked in this repo, not yours).

If you need project-specific agent instructions, create a separate directory:

```
my_project/
├── .agents/              ← submodule (shared base)
├── .agents_local/        ← your project-specific overrides (gitignored or committed)
│   └── project_rules.md
└── ...
```

## Versioning

Pin to a specific version by checking out a tag in the submodule:

```bash
cd .agents
git checkout v1.0
cd ..
git add .agents
git commit -m "Pin AI instructions to v1.0"
```