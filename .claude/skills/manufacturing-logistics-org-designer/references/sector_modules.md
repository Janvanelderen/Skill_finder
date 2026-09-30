# Sector modules: constraints, extra roles, agent guardrails

Read the section that matches the company. Constraints listed here become **hard guardrails** in the agent cards.

## Food & beverage (`"sector_module": "food"`)
- **Extra roles** (added by the script): a hygiene/sanitation crew (~0.7 FTE per line-shift, plus weekend deep clean) and a QC lab / line QC (~2 per shift). Add NPD (product/packaging development) and utilities technicians if relevant.
- **Structure**: Quality & Food Safety reports to the MD, not to the plant. Batch release must be independent of output targets, and IFS/BRCGS auditors check for this.
- **Constraints**:
  - **Warehouse**: FEFO picking; minimum remaining shelf life (MRSL) per retailer at delivery; lot traceability one step up and one step down.
  - **Production**: allergen sequencing and cleaning validation between runs.
  - **Transport**: fixed retailer DC delivery slots; temperature control where applicable.
- **Agent guardrails**:
  - Agents may put product on QA hold but never release it.
  - Allergen and shelf-life master data changes need QA approval.
  - No truck leaves without QA release.
- **Typical extra agents**: Promo Uplift (retail promotions drive peaks), Shelf-life & Write-off agent, CCP/SPC monitor (feeds QA; alerts only).
- **Key KPIs**: write-offs % of revenue, MRSL rejections, OTIF per retailer, giveaway/overweight %, changeover (allergen clean) time.

## Metalworking / machine building (MTO/ETO)
- **Extra roles** (added by the script for MTO/ETO): Work Preparation & Costing (drawings, CAM/nesting, BOM and routing, quotation). This is often the hidden bottleneck, so plan it as a capacity. With a significant ETO share, add project management.
- **Constraints**:
  - Material certificates (EN 10204 3.1) must accompany material through production, and material without a certificate is never released.
  - Outsourced processes (coating, galvanising, machining) add 3–10 days and need track & trace.
  - Remnant sheet registration.
  - Welding capacity is often the bottleneck.
- **Agents**:
  - `quote-costing`: reads drawings, estimates routing and cost from similar parts, and proposes a price. Minimum-margin guard (e.g. ≥18%). Quotes above a value cap (e.g. €25k) are done manually.
  - `work-preparation`: drafts BOM, routing and nesting from CAD for repeat or similar parts.
  - `ctp-promiser`: capable-to-promise against bottleneck capacity plus material and subcontract lead times. Rush requests below X days escalate.
  - `subcontracting`: batches work per subcontractor (e.g. per RAL colour), monitors return dates and checks returns are complete.
  - Planning follows drum-buffer-rope on the bottleneck.
- **Key KPIs**: quote lead time, quote hit rate, OTD on promised date, lead time order→delivery, WIP value, nesting yield, subcontract lead time.

## Pharma / medical (GMP)
- Like food, plus: QP batch release is never delegated. Computer system validation (GAMP 5) applies to agents that touch GMP records, so keep agents advisory (L0–L1) on GMP data unless validated. Serialisation.

## Automotive supplier (JIT/JIS)
- Call-offs via EDI (DELFOR/DELJIT); line-feed sequencing; premium freight is the key cost KPI. Agents: call-off analysis, premium-freight prevention, packaging/returnables tracking. Standards: IATF 16949, VDA.

## Chemicals / process industry
- ADR/dangerous goods, bulk (silos/tanks), campaign planning. Agent guardrails: never plan ADR loads without DG-check; the HSE owner signs off.
