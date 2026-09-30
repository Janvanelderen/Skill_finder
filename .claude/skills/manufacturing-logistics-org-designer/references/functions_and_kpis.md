# Function catalogue, reporting lines and KPIs

Default top structure for a logistics-driven manufacturer (single legal entity, 1–3 sites):

```
Managing Director / CEO
├── Supply Chain Director
│   ├── Demand & Supply Planning (S&OP, demand planning, MPS/MRP, scheduling)
│   ├── Procurement & Supplier Management
│   ├── Warehousing (inbound, storage, picking, packing, shipping, inventory control)
│   ├── Transport & Distribution (own fleet and/or carrier management, planning, yard)
│   └── Customer Service / Order Management
├── Operations / Plant Director
│   ├── Production (per line/cell or per shift)
│   ├── Maintenance & Engineering
│   └── Continuous Improvement (Lean / Six Sigma)
├── Quality & HSE (QA/QC, certification, safety, environment)
├── Commercial (Sales, Account Management, Marketing)
├── Finance & Control (incl. cost accounting, inventory valuation)
├── HR
└── IT & Data (ERP/WMS/TMS/MES, data platform, AI/agent operations)
```

Variants:
- **Small (<100 FTE)**: merge Planning and Procurement under one Supply Chain Manager; Quality + HSE is one role; IT is 1–2 FTE or outsourced.
- **Multi-site**: central Planning, Procurement, Customer Service and Transport planning; local Warehouse and Plant management; a dotted line from local warehouse managers to the SC Director.
- **ETO/project manufacturing**: add Project Management / Order Engineering between Sales and Production; planning is project-based (milestones) instead of MRP-driven.
- **Heavy outsourcing of logistics (3PL)**: replace Warehousing/Transport operational teams with a Logistics Service Provider Manager + contract/performance management.

## Function details

| Function | Core responsibilities | Key KPIs (typical targets) | Main systems |
|---|---|---|---|
| S&OP / Demand planning | Monthly S&OP, statistical forecast, consensus demand plan | Forecast accuracy (1 − WMAPE) at SKU-month 70–85%; bias ±5% | ERP/APS, BI |
| Supply planning / MRP | MPS, MRP runs, safety stocks, capacity check | Schedule adherence ≥95%; inventory turns (industry-dependent, 4–12) | ERP/APS |
| Production scheduling | Daily/shift sequence, changeover optimisation | Schedule attainment ≥90%; changeover time | MES/APS |
| Procurement | Sourcing, contracts, PO management, supplier performance | Supplier OTIF ≥95%; PPV; spend under contract ≥80% | ERP, e-procurement |
| Warehousing | Receiving, putaway, replenishment, picking, packing, shipping, cycle counts | Inventory record accuracy ≥98%; order lines/picker-hour; dock-to-stock <24h; picking error rate <0.3% | WMS |
| Transport | Route planning, carrier selection/tendering, freight audit, yard | On-time delivery ≥95%; cost per pallet/drop; load factor ≥80%; CO₂ per tonne-km | TMS, telematics |
| Customer service | Order entry, order promising (ATP/CTP), complaints, delivery info | OTIF to customer ≥95%; order-entry lead time; first-contact resolution | ERP, CRM |
| Production | Output, labour deployment, first-line quality | OEE 60–85%; scrap %; labour productivity | MES |
| Maintenance | Preventive/predictive maintenance, breakdowns | MTBF, MTTR, planned vs unplanned ratio ≥80/20 | CMMS |
| Quality & HSE | QA/QC, audits, CAPA, safety | Customer PPM, CAPA closure time, LTIFR | QMS |
| Finance | Cost price, inventory valuation, working capital | Cash conversion cycle, inventory days | ERP |
| IT & Data | Systems, master data, data platform, agent operations | Master-data quality ≥98%, system uptime, agent uptime | all |

## Key cross-functional decisions (RACI candidates)

| Decision | Typical R | Typical A |
|---|---|---|
| Consensus demand plan | Demand Planner | SC Director |
| Production plan freeze (frozen zone) | Supply Planner | Plant Director |
| Safety-stock / reorder-point change | Supply Planner | SC Director |
| Customer order promise date (non-standard) | Customer Service | SC Director |
| Carrier selection / tender award | Transport Manager | SC Director |
| New supplier onboarding | Buyer | Procurement Manager |
| Stock write-off / obsolescence | Inventory Controller | Finance Director |
| Agent autonomy level change | Agent owner | SC Director + IT & Data |
