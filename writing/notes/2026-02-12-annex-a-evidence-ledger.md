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
- **Evidence extracted:** Reports shift from monolithic C2 ambition to tactical software and kill-chain compression; executive findings describe unmanned systems conducting up to 80% of Russian fire missions in observed contexts and software workflows that reduce detection-to-impact from hours to minutes.
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

### E-012 — Reuters infrastructure reporting [29][31][32]
- **Topic cluster(s):** Infrastructure, power, industrial constraints
- **Evidence extracted:** Reports gigawatt-class and multi-billion-dollar data center expansion race dynamics; highlights financing/capital-structure pressure as a core scaling factor; also reports explicit mitigation steps for grid upgrade cost pass-through and local energy burden concerns.
- **Analytical use:** Shows compute and power are immediate deployment constraints with social and regulatory implications.
- **Deduction:** ACP-RA should include compute-tier and degraded-mode design assumptions; DAD should add infrastructure readiness criteria to scale approvals.
- **Confidence + limits:** Medium-high confidence for reported facts; news reporting snapshots do not replace longitudinal infrastructure data.
- **Follow-up actions:** Add power-demand and regional-grid risk models where available.


### E-013 — CNAS Countering the Swarm full report [54]
- **Topic cluster(s):** Swarms, C-UAS force design
- **Evidence extracted:** States cheap-drone proliferation has democratized mass precision fires and warns future conflict will present unavoidable drone threat to U.S. forces; recommends layered active/passive defenses, expanded counter-drone training, and AI-enabled C-UAS kill-chain acceleration.
- **Analytical use:** Provides force-design-level recommendations with practical readiness implications beyond high-level threat framing.
- **Deduction:** ACP-RA must include saturation and layered-defense logic in command workflows, with specific controls for high-volume attack conditions.
- **Confidence + limits:** High confidence in directional findings; implementation-cost and theater-specific constraints still require quantitative modeling.
- **Follow-up actions:** Extract CNAS recommended capability phasing into ACP-RA control requirement matrix.

### E-014 — RAND strategic competition study [39]
- **Topic cluster(s):** Strategic uncertainty, adversarial adaptation
- **Evidence extracted:** Identifies deep uncertainty in strategic AI effects and prioritizes iterative reassessment as evidence improves; emphasizes rapid adaptation against intensifying competition.
- **Analytical use:** Supports dynamic governance and model revision cycles rather than static doctrine assumptions.
- **Deduction:** DAD oversight should be cyclical and evidence-refresh driven.
- **Confidence + limits:** High confidence on strategic framing; limited direct implementation detail.
- **Follow-up actions:** Define review cadence and trigger criteria for DAD policy updates.

### E-015 — UK MOD JSP 936 policy directive [41]
- **Topic cluster(s):** Governance implementation
- **Evidence extracted:** Positions JSP 936 as principal policy framework for safe/responsible AI adoption, spanning governance, lifecycle development, and assurance with human oversight requirements.
- **Analytical use:** Demonstrates institutional codification of responsible AI requirements in defense organizations.
- **Deduction:** DAD should issue directive-grade governance requirements with lifecycle assurance obligations.
- **Confidence + limits:** High confidence on policy intent; practical compliance performance data still limited.
- **Follow-up actions:** Compare JSP lifecycle controls against ACP-RA control primitives.

### E-016 — UK MOD RAISO report [42]
- **Topic cluster(s):** Organizational accountability
- **Evidence extracted:** Describes Responsible AI Senior Officer appointments across MOD components to ensure local processes, escalation paths, and ethical-principle compliance.
- **Analytical use:** Offers concrete governance pattern for institutional accountability distribution.
- **Deduction:** DAD should establish named accountable officers for autonomy governance in each major component.
- **Confidence + limits:** Medium-high confidence; self-reported implementation maturity.
- **Follow-up actions:** Build RAISO-equivalent role architecture for DAD operating model.

### E-017 — UNODA / UNGA 79/239 process [44]
- **Topic cluster(s):** International governance
- **Evidence extracted:** Notes first General Assembly resolution focused on AI in the military domain, affirming international law applicability across lifecycle stages and calling for bridging governance divides.
- **Analytical use:** Establishes global governance trajectory and legal framing pressure.
- **Deduction:** DAD governance model should remain compatible with emerging multilateral norms and reporting expectations.
- **Confidence + limits:** High confidence on institutional process; limited operational specificity.
- **Follow-up actions:** Track A/80/78 and state submissions for convergent implementation standards.

### E-018 — SIPRI + ICRC accountability framing [45][46]
- **Topic cluster(s):** Legal accountability
- **Evidence extracted:** Emphasizes that machines cannot bear legal accountability; state and individual responsibility frameworks remain central and require clarified legal standards for practical enforcement.
- **Analytical use:** Reinforces need for architecture-level traceability and human accountability retention.
- **Deduction:** ACP-RA evidence trails are legal-operational requirements, not optional observability features.
- **Confidence + limits:** High confidence on legal framing; translation into operational control language requires explicit mapping.
- **Follow-up actions:** Map accountability doctrines to required audit/provenance artifacts.

### E-019 — A2A production hardening signals [50][51]
- **Topic cluster(s):** Interoperability maturity
- **Evidence extracted:** Enterprise multi-agent roadmaps emphasize orchestration controls and managed runtimes; A2A v0.3 introduces gRPC support, security-card signing, and broader SDK/deployment pathways.
- **Analytical use:** Shows interoperability is shifting from concept to production engineering.
- **Deduction:** ACP-RA should standardize trust-boundary controls at protocol level before broad agent federation.
- **Confidence + limits:** Medium-high confidence; vendor-source optimism risk.
- **Follow-up actions:** Validate security-card and signing assumptions against adversarial threat models.

### E-020 — AI and NC2/NC3 risk interaction [48]
- **Topic cluster(s):** High-consequence governance
- **Evidence extracted:** Argues human launch authority alone is insufficient risk control if AI-enabled upstream information systems produce compounding failures in nuclear decision support pathways.
- **Analytical use:** Extends governance requirement from decision authority to full information pipeline integrity.
- **Deduction:** DAD and ACP-RA must govern upstream data, model, and context channels for high-consequence domains.
- **Confidence + limits:** Medium confidence; analytical article rather than official doctrine.
- **Follow-up actions:** Add high-consequence information-integrity controls to ACP threat and assurance model.

---

## Gaps to close next

1. Build explicit counterevidence ledger entries for each topic (disconfirming evidence pass).
2. Add per-topic confidence weighting and contradiction tracking.
3. Reduce reference set into core/supporting/adjacent tiers for final publication draft.
4. Add quantitative metric extraction table (tempo, cost, survivability, readiness).
5. Produce publication-cut citation set with direct quote snippets for final narrative hardening.
