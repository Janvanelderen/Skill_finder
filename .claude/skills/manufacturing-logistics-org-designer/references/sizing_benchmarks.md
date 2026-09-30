# Sizing benchmarks (rules of thumb)

These ratios are **indicative starting values** from common logistics practice, not validated norms. They vary strongly with product type, automation level and IT maturity. Always present results as a first-cut estimate and calibrate against the company's own data (timestudies, WMS productivity reports). `scripts/size_org.py` uses these defaults; override them in the profile under `"benchmarks"`.

## Productive hours

| Parameter | Default | Note |
|---|---|---|
| Operators per line-shift | 5 (profile default) | **Calibrate first**: food/packaging lines are often 6–10; CNC cells 1–3 |
| Contract hours per FTE per year | 1,720 | NL full-time ≈ 38–40 h/week |
| Productive hours per FTE per year | 1,450 | After holidays, sickness (~5%), training and breaks |
| Operating days per year | 250 | 5-day operation; use 300+ for 6-day/continuous |

## Warehouse productivity (per productive hour)

| Activity | Manual | Semi-automated | Highly automated (goods-to-person) |
|---|---|---|---|
| Order lines picked | 60 | 120 | 350 |
| Pallets received and put away | 12 | 18 | 30 |
| Pallets loaded (outbound) | 15 | 20 | 30 |

Add ~15% indirect warehouse time (replenishment, cycle counting, returns, housekeeping) unless modelled separately.

## Office/planning ratios

| Role | Driver | Default ratio |
|---|---|---|
| Demand planner | Active SKUs | 1 FTE per 1,000 SKUs (min 1) |
| Supply planner / MRP | Active SKUs + components | 1 FTE per 800 SKUs (min 1) |
| Production scheduler | Production lines × shifts | 1 FTE per 6 line-shifts (min 1) |
| Buyer | Active suppliers | 1 FTE per 150 suppliers (min 1) |
| Customer service | Orders per day | 1 FTE per 60 orders/day (min 1) |
| Transport planner | Trucks dispatched per day | 1 FTE per 25 trucks/day (min 0.5) |
| Driver (own fleet) | Vehicles × shifts | 1.2 FTE per vehicle per shift (covers leave) |
| Inventory controller | Warehouse pallet locations | 1 FTE per 10,000 locations (min 0.5) |
| Master-data specialist | Active SKUs | 1 FTE per 5,000 SKUs (min 0.5) |
| Customer service with EDI | EDI share of orders | an EDI order counts as 0.4 of a manual order |
| Work preparation & costing (MTO/ETO) | Orders per year | 2 FTE per 1,000 orders/yr, +50% × ETO share |
| Process/CI engineer | Production lines | 0.8 FTE per line (min 1) |
| Food: hygiene crew | Line-shifts | 0.7 FTE per line-shift |
| Food: QC lab / line QC | Shifts | 2 FTE per shift |

Small-company variant (< 150 FTE): one Supply Chain & Logistics Manager replaces the SC Director and the Planning/Procurement/CS/Transport/Warehouse managers; one Operations Manager replaces the Plant Director and Production Manager.

## Spans of control

| Level | Range | Default |
|---|---|---|
| Team leader : operators/drivers (warehouse, production) | 10–15 | 12 |
| Supervisor/shift manager : team leaders | 3–6 | 4 |
| Office manager : specialists | 6–10 | 8 |

## Agent effect assumptions (for FTE range estimates)

Present these only as ranges, phased by roadmap wave, and only after a pilot has measured the effect.

| Area | Typical effect of mature agent support |
|---|---|
| Customer service order entry and delivery-status questions | 20–40% time saving |
| Demand planning (statistical baseline + exception handling) | 15–30% |
| Procurement PO follow-up / expediting | 20–35% |
| Transport planning (route/load optimisation + tender) | 10–25% |
| Warehouse floor labour | 0–5% (agents barely move physical work; automation/robotics does) |
