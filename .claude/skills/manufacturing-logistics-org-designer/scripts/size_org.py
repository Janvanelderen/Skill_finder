#!/usr/bin/env python3
"""First-cut org sizing + agent catalogue skeleton for a manufacturing/logistics company.

Usage:
    python3 size_org.py profile.json --out outdir/

Reads a company profile (see assets/company_profile_template.json), applies the
benchmark ratios from references/sizing_benchmarks.md (overridable via the
profile's "benchmarks" key) and writes:
    org_sizing.json      FTE per function/role, spans, drivers, assumptions
    org_chart.mmd        Mermaid org chart
    agent_catalogue.json agent skeleton with owner, autonomy and default parameters

Stdlib only. All numbers are rules of thumb: calibrate with real data.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DEFAULT_BENCHMARKS = {
    "productive_hours_per_fte": 1450,
    "pick_lines_per_hour": {"manual": 60, "semi": 120, "high": 350},
    "receive_pallets_per_hour": {"manual": 12, "semi": 18, "high": 30},
    "load_pallets_per_hour": {"manual": 15, "semi": 20, "high": 30},
    "warehouse_indirect_pct": 0.15,
    "skus_per_demand_planner": 1000,
    "skus_per_supply_planner": 800,
    "line_shifts_per_scheduler": 6,
    "suppliers_per_buyer": 150,
    "orders_per_day_per_cs_fte": 60,
    "trucks_per_day_per_transport_planner": 25,
    "driver_fte_per_vehicle_shift": 1.2,
    "locations_per_inventory_controller": 10000,
    "skus_per_master_data_fte": 5000,
    "production_cover_factor": 1.2,
    "operators_per_maintenance_tech": 20,
    "ops_fte_per_quality_fte": 40,
    "span_team_leader": 12,
    "span_supervisor": 4,
    "span_office_manager": 8,
    # support functions as share of all other FTE
    "finance_pct": 0.025,
    "hr_pct": 0.015,
    "it_pct": 0.02,
    "commercial_fte_per_eur_m": 0.15,
}

# agent id -> (name, owner role, start autonomy, required systems, min company FTE)
AGENTS = [
    ("sop-orchestrator", "S&OP Orchestrator", "Supply Chain Director", "L1", ["erp"], 100),
    ("demand-forecaster", "Demand Forecast Agent", "Demand Planner", "L2", ["erp"], 0),
    ("supply-planner", "Supply Planning Agent", "Supply Planner", "L2", ["erp"], 100),
    ("production-scheduler", "Scheduling Agent", "Production Scheduler", "L1", ["erp"], 100),
    ("procurement-buyer", "Procurement Agent", "Procurement Manager", "L2", ["erp"], 0),
    ("inbound-coordinator", "Inbound & Dock Agent", "Warehouse Manager", "L2", ["wms"], 100),
    ("inventory-controller", "Inventory Control Agent", "Inventory Controller", "L2", ["wms"], 100),
    ("replenishment", "Replenishment Agent", "Warehouse Manager", "L3", ["wms"], 250),
    ("wave-planner", "Wave & Labour Planning Agent", "Warehouse Shift Manager", "L1", ["wms"], 250),
    ("transport-planner", "Transport Planning Agent", "Transport Manager", "L2", ["tms"], 100),
    ("freight-auditor", "Freight Audit Agent", "Transport Manager", "L3", ["tms"], 100),
    ("order-promiser", "Order Promising Agent", "Customer Service Manager", "L2", ["erp"], 100),
    ("customer-service", "Customer Service Agent", "Customer Service Manager", "L3 info / L1 changes", ["erp"], 0),
    ("maintenance-advisor", "Maintenance Agent", "Maintenance Manager", "L1", ["cmms"], 250),
    ("quality-agent", "Quality Agent", "Quality & HSE Manager", "L1", ["qms"], 250),
    ("master-data-steward", "Master Data Agent", "Master Data Specialist", "L2", ["erp"], 0),
    ("control-tower", "Supply Chain Control Tower", "Supply Chain Director", "L1", ["erp"], 250),
]

MODEL_TIER = {
    "sop-orchestrator": "large", "production-scheduler": "large", "control-tower": "large",
    "supply-planner": "large", "transport-planner": "large",
    "freight-auditor": "small", "inbound-coordinator": "small", "master-data-steward": "small",
    "replenishment": "small",
}
TEMPERATURE = {"customer-service": 0.3, "quality-agent": 0.3, "sop-orchestrator": 0.2}


def r1(x: float) -> float:
    return round(x, 1)


def heads(x: float, minimum: float = 0) -> float:
    """Round FTE to 0.5 steps, with a minimum."""
    return max(minimum, math.ceil(x * 2) / 2) if x > 0 else minimum


def leaders(operators: float, span: int, shifts: int) -> int:
    if operators <= 0:
        return 0
    return max(math.ceil(operators / span), shifts if operators >= span else 1)


def size(profile: dict) -> dict:
    b = {**DEFAULT_BENCHMARKS, **profile.get("benchmarks", {})}
    auto = profile.get("automation_level", "manual")
    hrs = b["productive_hours_per_fte"]
    days = profile.get("operating_days", 250)
    shifts = profile.get("shifts_per_day", 1)
    sites = profile.get("sites", 1)
    g = profile.get

    fn: dict[str, dict] = {}

    def add(function, role, fte, driver, parent_role=None):
        fn.setdefault(function, {"roles": []})["roles"].append(
            {"role": role, "fte": r1(fte), "driver": driver, "reports_to": parent_role})

    # Warehousing
    pick = g("order_lines_per_day", 0) * days / (b["pick_lines_per_hour"][auto] * hrs)
    recv = g("inbound_pallets_per_day", 0) * days / (b["receive_pallets_per_hour"][auto] * hrs)
    load = g("outbound_pallets_per_day", 0) * days / (b["load_pallets_per_hour"][auto] * hrs)
    direct = pick + recv + load
    wh_ops = heads(direct * (1 + b["warehouse_indirect_pct"]))
    wh_tl = leaders(wh_ops, b["span_team_leader"], shifts)
    wh_sm = math.ceil(wh_tl / b["span_supervisor"]) if wh_tl > b["span_supervisor"] else 0
    add("Warehousing", "Warehouse Operator", wh_ops,
        f"pick {r1(pick)} + receive {r1(recv)} + load {r1(load)} FTE direct, +{int(b['warehouse_indirect_pct']*100)}% indirect ({auto})",
        "Warehouse Team Leader")
    add("Warehousing", "Warehouse Team Leader", wh_tl, f"span 1:{b['span_team_leader']}, min 1 per shift",
        "Warehouse Shift Manager" if wh_sm else "Warehouse Manager")
    if wh_sm:
        add("Warehousing", "Warehouse Shift Manager", wh_sm, f"span 1:{b['span_supervisor']} team leaders", "Warehouse Manager")
    inv = heads(g("warehouse_locations", 0) / b["locations_per_inventory_controller"], 0.5 if wh_ops else 0)
    add("Warehousing", "Inventory Controller", inv, f"{g('warehouse_locations', 0)} locations", "Warehouse Manager")
    add("Warehousing", "Warehouse Manager", sites, "1 per site", "Supply Chain Director")

    # Transport
    tp = heads(g("trucks_per_day", 0) / b["trucks_per_day_per_transport_planner"], 0.5 if g("trucks_per_day", 0) else 0)
    drivers = g("own_fleet_vehicles", 0) * g("fleet_shifts", 1) * b["driver_fte_per_vehicle_shift"]
    add("Transport", "Transport Planner", tp, f"{g('trucks_per_day', 0)} trucks/day", "Transport Manager")
    if drivers:
        add("Transport", "Driver", heads(drivers), f"{g('own_fleet_vehicles')} vehicles x {g('fleet_shifts', 1)} shift(s) x {b['driver_fte_per_vehicle_shift']}", "Fleet Team Leader")
        add("Transport", "Fleet Team Leader", leaders(drivers, b["span_team_leader"], 1), f"span 1:{b['span_team_leader']}", "Transport Manager")
    add("Transport", "Transport Manager", 1, "outsourced carriers" if not drivers else "own fleet + carriers", "Supply Chain Director")

    # Planning
    skus = g("active_skus", 0)
    add("Planning", "Demand Planner", heads(skus / b["skus_per_demand_planner"], 1), f"{skus} SKUs", "Planning Manager")
    add("Planning", "Supply Planner", heads(skus / b["skus_per_supply_planner"], 1), f"{skus} SKUs", "Planning Manager")
    line_shifts = g("production_lines", 0) * shifts
    add("Planning", "Production Scheduler", heads(line_shifts / b["line_shifts_per_scheduler"], 1), f"{line_shifts} line-shifts", "Planning Manager")
    add("Planning", "Planning Manager", 1, "owns S&OP process", "Supply Chain Director")

    # Procurement
    sup = g("active_suppliers", 0)
    add("Procurement", "Buyer", heads(sup / b["suppliers_per_buyer"], 1), f"{sup} suppliers", "Procurement Manager")
    add("Procurement", "Procurement Manager", 1, "", "Supply Chain Director")

    # Customer service
    opd = g("orders_per_day", 0)
    add("Customer Service", "Customer Service Agent (human)", heads(opd / b["orders_per_day_per_cs_fte"], 1), f"{opd} orders/day", "Customer Service Manager")
    add("Customer Service", "Customer Service Manager", 1, "", "Supply Chain Director")

    # Production
    ops = g("production_operators") or g("production_lines", 0) * shifts * g("operators_per_line_shift", 5) * b["production_cover_factor"]
    ops = heads(ops)
    p_tl = leaders(ops, b["span_team_leader"], shifts)
    p_sm = math.ceil(p_tl / b["span_supervisor"]) if p_tl > b["span_supervisor"] else 0
    add("Production", "Production Operator", ops,
        "given" if g("production_operators") else f"{g('production_lines', 0)} lines x {shifts} shifts x {g('operators_per_line_shift', 5)} x cover {b['production_cover_factor']}",
        "Production Team Leader")
    add("Production", "Production Team Leader", p_tl, f"span 1:{b['span_team_leader']}", "Production Shift Manager" if p_sm else "Production Manager")
    if p_sm:
        add("Production", "Production Shift Manager", p_sm, f"span 1:{b['span_supervisor']}", "Production Manager")
    add("Production", "Production Manager", sites, "1 per site", "Plant Director")

    # Maintenance / Quality
    add("Maintenance", "Maintenance Technician", heads(ops / b["operators_per_maintenance_tech"], 1), f"1 per {b['operators_per_maintenance_tech']} operators", "Maintenance Manager")
    add("Maintenance", "Maintenance Manager", 1, "", "Plant Director")
    q = heads((ops + wh_ops) / b["ops_fte_per_quality_fte"], 1)
    add("Quality & HSE", "QA/HSE Specialist", q, f"1 per {b['ops_fte_per_quality_fte']} ops FTE", "Quality & HSE Manager")
    add("Quality & HSE", "Quality & HSE Manager", 1, "", "Managing Director")

    # Data
    add("IT & Data", "Master Data Specialist", heads(skus / b["skus_per_master_data_fte"], 0.5), f"{skus} SKUs", "IT & Data Manager")

    subtotal = sum(r["fte"] for f in fn.values() for r in f["roles"])
    fin = heads(subtotal * b["finance_pct"], 1)
    hr = heads(subtotal * b["hr_pct"], 1)
    it = heads(subtotal * b["it_pct"], 1)
    com = heads(g("revenue_eur_m", 0) * b["commercial_fte_per_eur_m"], 1)
    add("IT & Data", "IT & Data Manager", 1, "incl. agent operations", "Managing Director")
    add("IT & Data", "IT Specialist", it, f"{int(b['it_pct']*1000)/10}% of FTE", "IT & Data Manager")
    add("Finance & Control", "Finance Staff", fin, f"{b['finance_pct']*100}% of FTE", "Managing Director")
    add("HR", "HR Staff", hr, f"{b['hr_pct']*100}% of FTE", "Managing Director")
    add("Commercial", "Sales & Account Management", com, f"{b['commercial_fte_per_eur_m']} FTE per EUR m revenue", "Managing Director")
    add("Management", "Managing Director", 1, "", None)
    add("Management", "Supply Chain Director", 1, "", "Managing Director")
    add("Management", "Plant Director", 1, "", "Managing Director")

    for f in fn.values():
        f["fte_total"] = r1(sum(r["fte"] for r in f["roles"]))
    total = r1(sum(f["fte_total"] for f in fn.values()))

    checks = []
    known = g("total_fte_known")
    if known:
        dev = (total - known) / known
        checks.append({"check": "total vs known headcount", "calculated": total, "known": known,
                       "deviation_pct": round(dev * 100, 1),
                       "status": "OK" if abs(dev) <= 0.25 else "RECONCILE: check automation level / productivity / operators per line"})

    return {"company": g("company_name"), "total_fte": total, "functions": fn,
            "checks": checks, "assumptions": g("assumptions", []), "benchmarks_used": b}


def agents(profile: dict, total_fte: float) -> list[dict]:
    systems = profile.get("systems", {})
    out = []
    for aid, name, owner, level, req, min_fte in AGENTS:
        missing = [s for s in req if not systems.get(s)]
        if total_fte < min_fte:
            status = f"later wave (recommended from ~{min_fte} FTE)"
        elif missing:
            status = f"blocked: needs {', '.join(missing).upper()}"
        else:
            status = "recommended"
        out.append({
            "id": aid, "name": name, "owner": owner, "autonomy_level": level,
            "status": status, "required_systems": req,
            "parameters": {
                "model_tier": MODEL_TIER.get(aid, "medium"),
                "temperature": TEMPERATURE.get(aid, 0.1),
                "confidence_threshold": 0.85,
                "human_review_sample_pct": 10,
            },
        })
    return out


def mermaid(sizing: dict) -> str:
    lines = ["flowchart TD"]
    nodes = {}
    for fname, f in sizing["functions"].items():
        for r in f["roles"]:
            nid = "n" + str(len(nodes))
            nodes[r["role"]] = (nid, r)
    for role, (nid, r) in nodes.items():
        label = f"{role}<br/>{r['fte']} FTE" if r["fte"] != 1 else role
        lines.append(f'    {nid}["{label}"]')
    for role, (nid, r) in nodes.items():
        parent = r["reports_to"]
        if parent and parent in nodes:
            lines.append(f"    {nodes[parent][0]} --> {nid}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("profile")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    profile = json.loads(Path(a.profile).read_text())
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    sizing = size(profile)
    cat = agents(profile, sizing["total_fte"])
    (out / "org_sizing.json").write_text(json.dumps(sizing, indent=2, ensure_ascii=False))
    (out / "org_chart.mmd").write_text(mermaid(sizing))
    (out / "agent_catalogue.json").write_text(json.dumps(cat, indent=2, ensure_ascii=False))

    print(f"Total FTE (first cut): {sizing['total_fte']}")
    for name, f in sizing["functions"].items():
        print(f"  {name:<18} {f['fte_total']:>6}")
    for c in sizing["checks"]:
        print(f"CHECK {c['check']}: {c['calculated']} vs {c['known']} ({c['deviation_pct']}%) -> {c['status']}")
    rec = [x["id"] for x in cat if x["status"] == "recommended"]
    print(f"Agents recommended now: {len(rec)} -> {', '.join(rec)}")
    print(f"Written to {out}/")


if __name__ == "__main__":
    main()
