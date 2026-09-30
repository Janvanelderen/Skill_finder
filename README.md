# Skill_finder
Skills.ch skill finder

## Skills in this repo (`.claude/skills/`)

| Skill | Source | Purpose |
|---|---|---|
| `manufacturing-logistics-org-designer` | custom (this repo) | Org structure + AI-agent catalogue (roles, skills, tools, autonomy, parameters) for manufacturing/logistics companies. Run `python3 scripts/size_org.py profile.json --out out/` for first-cut FTE sizing. |
| `chro-advisor`, `company-os`, `coo-advisor`, `agent-designer`, `process-mapper`, `capacity-planner` | alirezarezvani/claude-skills | Org design, operating model, ops, multi-agent architecture, process mapping, capacity |
| `team-composition-patterns` | wshobson/agents | Claude Code agent-team composition |

Restore third-party skills with `npx skills experimental_install` (uses `skills-lock.json`).
