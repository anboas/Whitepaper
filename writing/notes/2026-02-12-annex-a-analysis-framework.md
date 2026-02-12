---
title: "Annex A Research Extraction Framework"
date: 2026-02-12
status: draft
type: note
summary: "Ontology-first framework for aligning sources, evidence extraction, and topic-level analysis for ACP-RA and DAD." 
---

## Goal hierarchy

1. Build a source-aligned knowledge base for ACP-RA architecture design.
2. Build a source-aligned knowledge base for DAD authority and governance design.
3. Preserve narrative quality by separating extraction from synthesis.

## Topic architecture

### T1 — Mission Control and C2 Compression
- Focus: decision-to-effect latency, command integrity, cross-domain integration.

### T2 — Swarm Operations and Force Survivability
- Focus: attritable mass, counter-swarm operations, force-wide resilience under volume attacks.

### T3 — Interoperability and Protocol Governance
- Focus: agent-to-agent standards, connector trust, orchestration control boundaries.

### T4 — Governance, Legal Accountability, and Responsible Use
- Focus: policy directives, legal responsibility, assurance/TEV&V, institutional accountability.

### T5 — Adversarial Resilience and Contested Operation
- Focus: supply-chain risk, adversarial adaptation cycles, stress behavior in degraded conditions.

### T6 — Compute, Power, and Industrial Constraints
- Focus: infrastructure economics, energy constraints, deployment bottlenecks, regional resilience.

## Source extraction schema (enumerated fields)

Each source card is populated with the following fields:

1. `source_id` — stable ontology identifier.
2. `citation_number` — paper reference number.
3. `title` — source title.
4. `url` — canonical link.
5. `source_type` — policy/report/news/vendor/blog/academic/etc.
6. `topic_primary` — one of T1–T6.
7. `topic_secondary` — optional cross-topic linkage.
8. `thesis_anchor` — which topic thesis this source most directly tests.
9. `evidence_narrative` — what the source actually contributes in narrative form.
10. `research_summary` — distilled interpretation of source significance.
11. `deduction_acp` — architecture implication for ACP-RA.
12. `deduction_dad` — institutional implication for DAD.
13. `counter_signal` — disconfirming or limiting signal from same source (if any).
14. `confidence` — high / medium-high / medium / low.
15. `extraction_depth` — L1 title signal, L2 page excerpt, L3 detailed extraction.
16. `status` — extracted / queued / blocked.
17. `last_updated` — timestamp for refresh cadence.

## Topic analysis structure

For each topic, analysis is built in this exact sequence:

1. **Topic thesis** (clear claim)
2. **Evidence stack** (source cards aligned to thesis)
3. **Consistency check** (where sources agree)
4. **Contradiction check** (where sources diverge)
5. **Operational deductions**
   - ACP-RA controls
   - DAD authorities
6. **Uncertainty register** (known unknowns)
7. **Collection plan** (what additional data is needed)

## Execution process

1. Register every source as an ontology `Document` node.
2. Assign each source to a primary topic node (T1–T6).
3. Populate full source-card fields in ontology properties.
4. Track extraction depth/status to separate complete vs provisional cards.
5. Maintain one active ingestion task for iterative batch updates.

## Quality gate (before synthesis)

A topic is synthesis-ready only if:

- at least 5 source cards are at extraction depth L2+, and
- at least 2 cards are independent/non-vendor sources, and
- at least 1 explicit counter-signal is documented.
