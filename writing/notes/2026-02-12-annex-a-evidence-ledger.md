---
title: "Annex A Evidence Ledger (Working)"
date: 2026-02-12
status: draft
type: note
summary: "Per-source evidence extraction log used to build the ACP mission-control research paper and DAD decision support memo."
---

## Purpose

This ledger is the extraction layer between raw links and paper prose.

For each source, we capture:
- what was actually observed,
- why it matters,
- what we infer,
- what still needs follow-up.

---

## Extraction template (locked)

- **Source ID + citation**
- **Topic cluster(s)**
- **Evidence extracted (facts/claims from source)**
- **Analytical use (how this supports or challenges thesis)**
- **Deduction**
- **Confidence + limits**
- **Follow-up actions**

---

## Current extraction pass

### E-001 — OpenAI Frontier [1]
- **Topic cluster(s):** Mission control, interoperability/governance
- **Evidence extracted:** States that enterprise bottleneck is no longer base model intelligence but how agents are built, deployed, and governed; emphasizes context, permissions, boundaries, and cross-system operation.
- **Analytical use:** Supports argument that control-plane engineering is now a primary bottleneck.
- **Deduction:** ACP-RA should prioritize deployment governance and boundary enforcement over model-centric optimization alone.
- **Confidence + limits:** High confidence on stated positioning; vendor source with promotional bias.
- **Follow-up actions:** Pair with third-party enterprise failure/implementation data.

### E-002 — Google A2A announcement [5]
- **Topic cluster(s):** Interoperability/protocol governance
- **Evidence extracted:** Introduces open A2A protocol with broad partner support; design principles include existing standards (HTTP/SSE/JSON-RPC), secure-by-default posture, long-running tasks, and modality agnosticism.
- **Analytical use:** Establishes protocol-level standardization trajectory in multi-agent ecosystems.
- **Deduction:** Trust and control will migrate toward protocol and identity boundaries.
- **Confidence + limits:** High confidence on protocol claims; consortium announcements can overstate adoption velocity.
- **Follow-up actions:** Track production deployments and interop failure modes.

### E-003 — Linux Foundation A2A governance move [52]
- **Topic cluster(s):** Interoperability/protocol governance
- **Evidence extracted:** A2A transferred into neutral Linux Foundation governance with major cloud/enterprise members; support base described as 100+ companies.
- **Analytical use:** Indicates movement from announcement phase to governance institutionalization.
- **Deduction:** DAD should define minimum protocol-control requirements before widespread cross-agent deployment.
- **Confidence + limits:** High confidence on governance event; adoption depth per member remains uneven.
- **Follow-up actions:** Monitor implementation compatibility and identity/security extensions.

### E-004 — GAO CJADC2 report [35]
- **Topic cluster(s):** Mission control and C2 compression
- **Evidence extracted:** Finds DOD lacks comprehensive CJADC2 framework with measurable goals; warns isolated service/entity efforts slow progress; recommends framework, lesson-sharing, and challenge remediation.
- **Analytical use:** Strong independent evidence that integration governance is an unresolved structural gap.
- **Deduction:** ACP-RA must be designed as an integration framework with measurable outcomes, not a disconnected pilot stack.
- **Confidence + limits:** High confidence (independent oversight source).
- **Follow-up actions:** Extract detailed GAO challenge taxonomy for direct ACP control requirements mapping.

### E-005 — CSIS Russia C2 analysis [37]
- **Topic cluster(s):** Mission control, adversarial adaptation
- **Evidence extracted:** Reports shift from monolithic C2 ambition to tactical software and kill-chain compression; describes high operational role of unmanned systems in fire missions and software-mediated targeting workflows.
- **Analytical use:** Demonstrates wartime adaptation logic under pressure and software-first battlefield optimization.
- **Deduction:** ACP-RA must assume adversary adaptation cycles are software-speed and continuous.
- **Confidence + limits:** Medium-high confidence; relies on open-source assessment of adversary systems.
- **Follow-up actions:** Cross-validate with additional battlefield telemetry analyses.

### E-006 — RAND future of war framework [38]
- **Topic cluster(s):** Mission command, resilience, force design
- **Evidence extracted:** Assesses AI effects on quantity/quality, hider/finder, C2 paradigms, and cyber offense/defense; recommends planning for adaptive adversaries and transition pathways.
- **Analytical use:** Supplies neutral conceptual framework for strategic architecture choices.
- **Deduction:** ACP-RA should be stress-tested against all four competitions, not only autonomous task success metrics.
- **Confidence + limits:** High confidence for framework-level analysis; not a direct implementation playbook.
- **Follow-up actions:** Build metric mapping from RAND dimensions to ACP eval suite.

### E-007 — DIU Replicator [47][56]
- **Topic cluster(s):** Swarms, acquisition and scale
- **Evidence extracted:** Replicator 1 targets multiple thousands of attritable autonomous systems in 18–24 months; Replicator 2 focuses on counter-sUAS and highlights policy/authority/production/system-integration constraints.
- **Analytical use:** Shows autonomy scale is a present acquisition reality, not future concept.
- **Deduction:** DAD authority must include rapid scale controls, standards, and risk gates aligned to accelerated acquisition tempo.
- **Confidence + limits:** Medium-high confidence; program messaging may emphasize positive progress.
- **Follow-up actions:** Pull budget/program execution data for throughput vs readiness quality.

### E-008 — CNA PRC UAV swarm concepts [55]
- **Topic cluster(s):** Swarms, threat adaptation
- **Evidence extracted:** Highlights PRC research/testing for autonomous swarm use in Taiwan scenarios and explicit attention to counter-swarm functions (detection, soft kill, hard kill, camouflage).
- **Analytical use:** Threat-side evidence that swarm and counter-swarm maturation is scenario-linked and operationally specific.
- **Deduction:** ACP-RA and DAD must treat swarm conflict as two-sided adaptation (offense + defense) in doctrine and evals.
- **Confidence + limits:** Medium-high confidence; inferential from open-source writings.
- **Follow-up actions:** Add force-on-force scenario assumptions for Taiwan and non-Taiwan theaters.

### E-009 — Army sustainment swarm note [53]
- **Topic cluster(s):** Swarms beyond maneuver, sustainment security
- **Evidence extracted:** Argues swarm/autonomous monitoring can offset manpower limits in convoy and support-area defense; cites large autonomous drone array example and continuous monitoring concept.
- **Analytical use:** Extends autonomy relevance into logistics and rear-area survivability.
- **Deduction:** ACP controls should be generalized across mission threads, not confined to kinetic strike workflows.
- **Confidence + limits:** Medium confidence; concept note, not controlled trial evidence.
- **Follow-up actions:** Seek empirical sustainment pilot outcomes and cost-benefit data.

### E-010 — NATO revised AI strategy summary [40]
- **Topic cluster(s):** Governance, TEV&V, interoperability
- **Evidence extracted:** Reaffirms responsible-use principles, highlights TEV&V landscape, interoperability objectives, adversarial-risk focus, and compute/energy implications.
- **Analytical use:** Alliance-level policy evidence that responsible adoption requires standards and verification infrastructure.
- **Deduction:** DAD should mandate evaluation and verification gates as deployment prerequisites.
- **Confidence + limits:** High confidence on policy direction; broad strategy language requires implementation specifics.
- **Follow-up actions:** Map NATO PRUs and TEV&V language to ACP control requirements.

### E-011 — U.S. Political Declaration page [43]
- **Topic cluster(s):** Governance/legal accountability
- **Evidence extracted:** Frames declaration as normative military-use framework; indicates ongoing plenary implementation among endorsing states.
- **Analytical use:** Confirms international governance trend toward practical implementation exchanges, not principle-only statements.
- **Deduction:** DAD should align internal governance artifacts with emerging partner-state responsible-use expectations.
- **Confidence + limits:** High confidence on declared process; limited operational detail in page text.
- **Follow-up actions:** Extract full declaration commitments and map to ACP provenance requirements.

### E-012 — Reuters infrastructure reporting [31][32]
- **Topic cluster(s):** Infrastructure, power, industrial constraints
- **Evidence extracted:** Reports gigawatt-class and multi-billion-dollar data center expansion race dynamics; also reports explicit mitigation steps for grid upgrade cost pass-through and local energy burden concerns.
- **Analytical use:** Shows compute and power are immediate deployment constraints with social and regulatory implications.
- **Deduction:** ACP-RA should include compute-tier and degraded-mode design assumptions; DAD should add infrastructure readiness criteria to scale approvals.
- **Confidence + limits:** Medium-high confidence for reported facts; news reporting snapshots do not replace longitudinal infrastructure data.
- **Follow-up actions:** Add power-demand and regional-grid risk models where available.

---

## Gaps to close next

1. Extract stronger quantitative evidence from GAO, RAND, and CSIS full PDFs.
2. Add direct evidence from CNAS full report text (currently blocked by PDF extraction limits in this pass).
3. Build explicit counterevidence ledger entries for each topic.
4. Add per-topic confidence weighting and contradiction tracking.
5. Reduce reference set into core/supporting/adjacent tiers for final publication draft.
