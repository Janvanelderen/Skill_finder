# Standard agent catalogue (manufacturing + logistics)

Pick from this list based on the profile. Don't include an agent unless its data source exists: an agent without clean input data only automates bad decisions. The ID in the first column is what `scripts/size_org.py` uses.

| ID | Agent | Function / owner | Start autonomy | Core job | Needs |
|---|---|---|---|---|---|
| `sop-orchestrator` | S&OP Orchestrator | SC Director | L1 | Prepares monthly S&OP pack: demand vs capacity vs inventory scenarios, gaps, decisions needed | ERP/APS read, BI |
| `demand-forecaster` | Demand Forecast Agent | Demand Planner | L2 | Statistical baseline forecast, outlier detection, flags SKUs with bias > threshold | 24+ months sales history |
| `supply-planner` | Supply Planning Agent | Supply Planner | L2 | MRP exception handling: proposes reschedule-in/out, expedite, cancel | ERP planned orders |
| `production-scheduler` | Scheduling Agent | Production Scheduler | L1 | Proposes shift sequences that minimise changeovers within due dates | MES/APS, routings, changeover matrix |
| `procurement-buyer` | Procurement Agent | Procurement Manager | L2→L3 | Converts approved requisitions into POs within caps, chases supplier confirmations, scores supplier OTIF | ERP PO write (capped), email/EDI |
| `inbound-coordinator` | Inbound & Dock Agent | Warehouse Manager | L2 | Dock-slot booking, ASN checking, deviation alerts | WMS, dock scheduling, ASN/EDI |
| `inventory-controller` | Inventory Control Agent | Inventory Controller | L2 | Cycle-count planning, discrepancy analysis, slotting proposals, obsolescence alerts | WMS read, ERP stock |
| `replenishment` | Replenishment Agent | Warehouse Manager | L3 | Pick-face replenishment tasks within min/max | WMS task write |
| `wave-planner` | Wave & Labour Planning Agent | Warehouse Shift Manager | L1 | Proposes pick waves and headcount per zone per shift | WMS order pool, labour data |
| `transport-planner` | Transport Planning Agent | Transport Manager | L2 | Load building, route optimisation, carrier choice within contract rates | TMS, rates, telematics |
| `freight-auditor` | Freight Audit Agent | Transport Manager + Finance | L3 | Matches carrier invoices against agreed rates, auto-approves within tolerance | TMS, AP invoices |
| `order-promiser` | Order Promising Agent | Customer Service Manager | L2 | ATP/CTP answers, proposes delivery dates, drafts order confirmations | ERP ATP, capacity |
| `customer-service` | Customer Service Agent | Customer Service Manager | L3 (info) / L1 (changes) | Answers where-is-my-order, delivery-document requests; drafts replies for changes/complaints | ERP, TMS track & trace, CRM |
| `maintenance-advisor` | Maintenance Agent | Maintenance Manager | L1 | Predictive alerts from sensor/CMMS data, work-order drafts | CMMS, IoT |
| `quality-agent` | Quality Agent | QA Manager | L1 | Nonconformity triage, CAPA drafting, supplier complaint drafts | QMS, inspection data |
| `master-data-steward` | Master Data Agent | IT & Data (Data Steward) | L2 | Detects missing/inconsistent master data (dimensions, lead times, MOQ) and proposes fixes | ERP/WMS master data read |
| `control-tower` | Supply Chain Control Tower | SC Director | L1 | Cross-functional exception feed: OTIF risks, stock-outs, late trucks; routes each to the right agent/owner | All read, event bus |

### Added automatically for MTO/ETO (see `sector_modules.md`)

| ID | Agent | Owner | Start autonomy | Core job | Needs |
|---|---|---|---|---|---|
| `quote-costing` | Quotation & Costing Agent | Work Preparation Manager | L1 | Routing/cost estimate from drawings and similar parts; price proposal with margin guard | ERP routings/costs, CAD |
| `work-preparation` | Work Preparation Agent | Work Preparation Manager | L2 | Drafts BOM/routing/nesting for repeat and similar parts | ERP, CAD/CAM |
| `ctp-promiser` | Capable-to-Promise Agent | Planning Manager | L1 | Delivery date from bottleneck capacity + material + subcontract lead times | ERP capacity, stock, supplier lead times |
| `subcontracting` | Subcontracting Agent | Procurement Manager | L2 | Batches outsourced work, monitors return dates/completeness, scores subcontractors | ERP, email/portal |

## Engine per agent

| Engine | Use for | Examples |
|---|---|---|
| Solver / APS (MILP, constraint programming, heuristics) | Feasible optimised plans | production-scheduler, transport-planner (routes/loads), wave-planner |
| Statistical / ML model | Forecasts and predictions | demand-forecaster, maintenance-advisor (failure probability) |
| LLM | Orchestration, explanation, exception triage, documents and communication | sop-orchestrator, control-tower, customer-service, quote-costing (text/drawing intake) |
| Rules | Deterministic checks | freight-auditor (rate match), inbound-coordinator (ASN check) |

Most agents combine engines: the LLM calls the solver or model as a tool and explains the result. Put this in the card as `engine:`.

## Orchestration pattern

Default: **hierarchical by planning horizon**
- Strategic/tactical: `sop-orchestrator` (monthly)
- Operational planning: `demand-forecaster`, `supply-planner`, `production-scheduler`, `transport-planner`, `wave-planner` (weekly/daily)
- Execution: `procurement-buyer`, `inbound-coordinator`, `replenishment`, `order-promiser`, `customer-service`, `freight-auditor`, `inventory-controller` (event-driven)
- Cross-cutting: `control-tower` (monitors, routes exceptions; does not execute), `master-data-steward`

Agents communicate through the systems of record (ERP/WMS/TMS) and an exception queue owned by the control tower, not through free-form chats with each other. That keeps an audit trail and a single source of truth.

## Minimum sets by company size

| Company size | Recommended starting set (wave 1) |
|---|---|
| < 100 FTE | `demand-forecaster`, `customer-service`, `procurement-buyer`, `master-data-steward` |
| 100–500 FTE | the above + `supply-planner`, `transport-planner`, `inventory-controller`, `control-tower` |
| > 500 FTE / multi-site | full catalogue, rolled out per site in waves |
