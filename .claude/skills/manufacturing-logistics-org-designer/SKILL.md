---
name: manufacturing-logistics-org-designer
description: "Design the organisation structure of a manufacturing company with a logistics/supply-chain focus AND the matching set of AI agents: functions, reporting lines, FTE sizing, spans of control, RACI, plus an agent catalogue with each agent's role, skills, tools/system access, autonomy level, parameters (model tier, temperature, thresholds, cadence), KPIs and human owner. Use this skill whenever the user wants an org chart, org design, target operating model, roles/FTE plan or agent/agentic-AI blueprint for a factory, plant, production company, warehouse, distribution centre, 3PL-like operation, supply chain or S&OP organisation — even if they only say 'set up agents for our production company', 'which AI agents do we need in logistics', 'design the organisation for our plant' or ask for agent parameters/configuration in a manufacturing or logistics context. Also use it for educational cases (students designing a fictitious manufacturing company). Not for pure software-company org design or generic multi-agent code architecture without an operations context."
---

# Manufacturing & Logistics Org + Agent Designer

Produce two linked designs for a manufacturing company whose competitive edge (or pain) sits in logistics:

1. **The human organisation**: functions, reporting lines, FTE per function, spans of control, decision rights.
2. **The agent layer**: which AI agents support which function, what each is allowed to do, with which tools and parameters, and which human owns it.

The two must be designed *together*: every agent has a human owner in the org chart, and every agent's autonomy is bounded by that owner's decision rights. An agent catalogue that floats free of the org chart is the most common failure: nobody is accountable when the replenishment agent orders 40 pallets too many.

## Workflow

### Step 1: Build the company profile (intake)

Fill `assets/company_profile_template.json`. Work from what the user gave you; for gaps, **make an explicit, plausible assumption and label it** rather than stopping to ask a long list of questions. Ask at most one focused question, and only if a missing fact changes the design fundamentally (typically: production strategy MTS/MTO/ETO, or whether transport is own fleet vs outsourced).

The drivers that matter most for sizing: annual revenue, total FTE (if known), production strategy, number of sites/DCs, shifts, SKU count, order lines per day (outbound), inbound pallets/trucks per day, own fleet size, number of suppliers, and the systems landscape (ERP/WMS/TMS/MES).

### Step 2: Size the organisation deterministically

Run the sizing script rather than estimating FTE by feel. It applies the benchmark ratios in `references/sizing_benchmarks.md` and returns FTE per function, the number of team leaders and managers from spans of control, and a Mermaid org chart:

```bash
python3 scripts/size_org.py profile.json --out <output_dir>
```

Outputs: `org_sizing.json` (FTE, managers, drivers, assumptions per function), `org_chart.mmd` (Mermaid), `agent_catalogue.json` (a skeleton with one line per recommended agent, owner pre-filled).

Treat the numbers as a **first-cut, benchmark-based estimate**, and say so. Sanity-check the result: if total FTE differs by more than ~25% from a headcount the user gave, reconcile it (usually the automation level or the productivity assumptions are off) and explain the gap instead of silently overriding either figure.

### Step 3: Design the structure

Read `references/functions_and_kpis.md` for the function catalogue, typical reporting lines and KPIs. Key choices to make and justify:

- **Where does Supply Chain sit?** An integrated Supply Chain Director (planning + procurement + warehousing + transport + customer service) reporting to the MD/COO is the default for logistics-driven manufacturers. Splitting logistics under Operations/Production only makes sense when logistics is small or purely plant-internal.
- **Planning hierarchy**: S&OP (monthly, tactical) → MPS/MRP (weekly) → scheduling (daily). Name who owns each horizon.
- **Centralised vs site-based**: with more than one site, decide per function (procurement and planning usually central; warehousing and maintenance local).
- **Spans of control**: shop floor/warehouse team leaders 10–15 operators, supervisors 3–6 team leaders, office managers 6–10. Flag any span outside these ranges.

Produce a RACI for the 6–10 key cross-functional decisions (e.g. demand plan sign-off, production schedule freeze, safety-stock changes, carrier selection, supplier onboarding, stock write-off, customer order promise date).

### Step 4: Design the agent layer

Read `references/agent_catalogue.md` for the standard agent set per function and `references/agent_parameters.md` for the parameter schema, defaults and autonomy levels.

For each agent specify the complete card (schema in `agent_parameters.md`): purpose, human owner (a role in the org chart), autonomy level (L0–L4), skills, tools and system access (read/write per system), trigger/cadence, parameters, guardrails with numeric thresholds, KPIs, escalation path and a fallback when the agent is down.

Design principles (and why):
- **Start with decision support, not autonomy.** Most agents start at L1–L2. Raise autonomy per agent only after a measured pilot, because mistakes in logistics turn into physical stock, trucks and penalties, which cost far more to undo than a bad email.
- **Write access to ERP/WMS/TMS is the real risk boundary.** Grant it narrowly (specific transaction types, value/quantity caps) and log every write.
- **Thresholds must be numbers.** Write "auto-release POs ≤ €2,500 and ≤ 110% of the forecast quantity", not "small orders".
- **One orchestrator per planning horizon**, not one agent that does everything: separate S&OP, daily planning and execution agents keep contexts clean and ownership clear.
- **Keep the human org lean where agents take load, but never remove the owner.** Show FTE effects as ranges (for example −0.5 to −1.5 FTE in customer service), phased over time, not as instant headcount cuts.

If `agent-designer` is installed, you can use its `agent_planner.py` for the orchestration pattern and `tool_schema_generator.py` for tool schemas. This skill stays responsible for the operational content.

### Step 5: Governance and roadmap

- **Governance**: agent owner, a monthly performance review (PDCA: plan KPI targets, run, check against a baseline, adjust parameters or autonomy), a change log for parameter changes, data-access review. Mention EU AI Act relevance where agents touch personnel (for example shift planning or performance monitoring of operators, which are high-risk HR uses) and GDPR for driver/operator data.
- **Roadmap** in 3 waves: (1) quick wins, read-only/advisory agents with clean data (0–3 months); (2) agents with limited write access in planning and warehousing (3–9 months); (3) cross-functional orchestration and higher autonomy (9–18 months). Each wave has entry criteria (data quality, KPI baseline measured) and an exit KPI.

## Output format

Deliver in this order (language: match the user's language):

1. **Company profile & assumptions**: table; mark assumptions explicitly.
2. **Org chart**: Mermaid diagram + a short rationale for the key structural choices.
3. **Roles & FTE table**: function | roles | FTE | span | key KPIs | sizing driver.
4. **RACI** for key decisions.
5. **Agent catalogue**: an overview table (agent | function | owner | autonomy | key tools | main KPI), then one agent card per agent in YAML (schema from `agent_parameters.md`).
6. **Governance & roadmap**: waves with entry/exit criteria.
7. **Open points / calibrate next**: the 3–5 assumptions that most affect the design.

When the user wants files, also save `org_sizing.json`, `org_chart.mmd`, `agent_catalogue.yaml` and a Markdown report to the output directory.

## Related installed skills

Use these for deeper dives when present: `chro-advisor` (comp, hiring plan), `company-os` (meeting cadence, scorecards), `coo-advisor` (process/OKR), `capacity-planner` (queueing-based staffing for customer service), `process-mapper` (value-stream/bottleneck mapping), `agent-designer` (orchestration pattern, tool schemas), `team-composition-patterns` (Claude Code agent teams).
