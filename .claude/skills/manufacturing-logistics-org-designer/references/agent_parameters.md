# Agent card schema, parameters and autonomy levels

## Autonomy levels

| Level | Name | The agent may | Human role | Typical use |
|---|---|---|---|---|
| L0 | Observe | Read data, report | Decides and acts | Dashboards, pilots |
| L1 | Advise | Propose options with rationale | Chooses, executes | S&OP, scheduling, maintenance |
| L2 | Prepare | Prepare transactions (draft PO, draft route); a human approves with one click | Approves each action | Planning, order promising |
| L3 | Act within limits | Execute autonomously within numeric guardrails; escalate outside them | Monitors, reviews exceptions + samples | Replenishment, freight audit, WISMO answers |
| L4 | Autonomous | Execute and self-adjust parameters within policy | Periodic audit | Rare in operations; only after 6+ months of stable L3 |

Rule: an agent's autonomy never exceeds the decision rights of its human owner.

## Parameter defaults

| Parameter | Meaning | Default guidance |
|---|---|---|
| `model_tier` | Capability/cost class | `large` for S&OP, scheduling, exception reasoning; `medium` for customer service and procurement; `small` for classification, extraction and matching (freight audit, ASN check) |
| `temperature` | Output variability | 0.0–0.2 for transactional and numeric work; 0.3–0.5 for drafting customer text; never >0.7 in operations |
| `max_output_tokens` | Output length cap | 1,000 for transactional; 4,000 for S&OP packs |
| `context_sources` | What it may read | List systems and tables explicitly |
| `write_permissions` | What it may change | Per system: transaction type + caps; default none |
| `trigger` | When it runs | `cron` (e.g. daily 05:30), `event` (e.g. ASN received), or `on_request` |
| `confidence_threshold` | Minimum confidence to act at L3 | 0.85 default; below → escalate |
| `value_cap_eur` | Max financial value per autonomous action | Procurement €2,500; freight audit tolerance ±2% or €50 |
| `quantity_cap_pct` | Max deviation vs plan/forecast | 110% of planned quantity |
| `rate_limit` | Max autonomous actions per period | e.g. 200 POs/day; protects against runaway loops |
| `human_review_sample_pct` | Share of autonomous actions reviewed | 10% in the first 3 months, then 2–5% |
| `escalation` | Who and how | Owner role + channel + SLA (e.g. 2 h in shift) |
| `fallback` | What happens if the agent is down | The manual procedure that stays in place |
| `logging` | Audit trail | All inputs, outputs, writes; 7-year retention for financial transactions |
| `review_cadence` | PDCA review | Monthly KPI review by owner; quarterly autonomy review |

## Agent card template (YAML)

```yaml
id: procurement-buyer
name: Procurement Agent
function: Procurement
owner: Procurement Manager            # must exist in the org chart
autonomy_level: L2                    # target after pilot: L3
purpose: >
  Convert approved purchase requisitions into purchase orders with preferred
  suppliers, obtain confirmations and flag late deliveries.
skills:
  - PO creation from requisitions and contracts
  - supplier confirmation follow-up (email/EDI)
  - supplier OTIF scoring
tools:
  - system: ERP
    access: read + write
    scope: create PO (doc type NB) for contracted items only
  - system: Email/EDI
    access: send
    scope: order confirmations and reminders to supplier contacts on file
trigger: event (requisition approved) + cron daily 07:00 (follow-up)
parameters:
  model_tier: medium
  temperature: 0.1
  max_output_tokens: 1000
  confidence_threshold: 0.85
  value_cap_eur: 2500
  quantity_cap_pct: 110
  rate_limit: 200 actions/day
  human_review_sample_pct: 10
guardrails:
  - never create POs for non-contracted suppliers
  - never change prices; price deviation > 0% escalates
  - never cancel POs with goods in transit
kpis:
  - PO cycle time requisition → PO < 4 h
  - supplier confirmation rate within 48 h ≥ 95%
  - buyer time saved 20–35% (measured vs baseline)
escalation: Buyer on duty, Teams channel #procurement-exceptions, SLA 4 h
fallback: buyers create POs manually in ERP (current procedure)
logging: all writes logged with requisition ID; retention 7 years
review_cadence: monthly KPI review (owner), quarterly autonomy review (SC Director + IT)
```

## Governance checklist

- Every agent has exactly one accountable owner (a role, not a person's name).
- Write permissions are listed per system with caps; everything else is read-only.
- A baseline KPI is measured *before* go-live; otherwise the effect cannot be proven.
- Parameter and autonomy changes go through a change log (who, what, why, date).
- EU AI Act: agents that allocate work or monitor/evaluate workers (shift planning, operator performance) fall under high-risk use and need extra documentation, human oversight and worker information. Involve the works council (OR) early in NL.
- GDPR: minimise personal data (drivers, operators, customer contacts); define retention.
