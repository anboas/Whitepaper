---
title: "CAF + ACP in Production: Joint Deployment Reference Pattern"
date: 2026-02-25
summary: "A deployment-grade architecture note showing how CAF-RA and ACP-RA run together using real tooling, custom control-plane components, and a live-fire production workload."
status: draft
type: note
tags:
  - caf-ra
  - acp-ra
  - deployment
  - control-planes
  - production
  - devsecops
  - governance
  - continuous-assurance
---

## Operating problem

Most enterprises can either move fast **or** stay governable under stress. They rarely do both.

When autonomous agents, CI/CD systems, and platform controllers can all trigger consequential changes, legacy governance breaks in one of two ways:
1. It becomes ceremonial and gets routed around.
2. It becomes approval drag and kills tempo.

CAF + ACP is the control-plane answer to that failure mode.

## Core assertion

**ACP governs action eligibility. CAF governs action advisability under current evidence and confidence. Enforcement points execute bounded effects. Verification closes the loop.**

That is the spine.

## What this pattern is, and what it is not

### It is
- A deployable architecture pattern for mission-tempo operations.
- A way to keep non-person principals fast but bounded.
- A method for producing replayable governance evidence, not just dashboards.

### It is not
- A product SKU.
- A one-time authorization event.
- A trust model where model output becomes authority.

## Joint architecture model (two planes, one doctrine)

### Plane A: Authority and action governance (ACP)
ACP defines who/what may act and under what explicit scope:
- attributable principal identity,
- trust scopes,
- signed authority manifests,
- signed policy bundles,
- mediated tool/action surfaces.

### Plane B: Continuous assurance and bounded execution (CAF)
CAF defines whether action is safe now and how tightly to constrain it:
- evidence emission and enrichment,
- confidence-bearing posture computation,
- supervised decision work units,
- consequence-tiered, mediated execution,
- independent verification and replay.

### Doctrine at the seam
- ACP prevents unauthorized action.
- CAF prevents unwise action under uncertainty.
- Decision records bind both.

## Loop contract in production terms

1. **EMIT**
   - Question: what changed, and who is asserting it?
   - Output: attributable, sealable evidence claims.
   - Unsafe failure mode: anonymous or spoofed producers.

2. **ENRICH**
   - Question: is this evidence admissible and replay-safe?
   - Output: normalized, labeled, anti-replay-validated envelopes.
   - Unsafe failure mode: poisoned/replayed evidence entering governance.

3. **SCORE**
   - Question: what is current posture, and how certain are we?
   - Output: confidence-bearing posture with evidence traceability.
   - Unsafe failure mode: opaque scoring treated as authority.

4. **SURFACE**
   - Question: what decision is pending, under which authority, with what evidence?
   - Output: supervised assurance work units.
   - Unsafe failure mode: dashboard theater disconnected from decisions.

5. **ACT**
   - Question: what bounded action is eligible now?
   - Output: mediated enforcement action + verification evidence.
   - Unsafe failure mode: unmediated side effects/runaway remediation.

## Tooling map (real-world stack)

### Off-the-shelf components
- **Identity/Auth:** Entra ID or Okta, workload identities, OIDC federation.
- **Policy/Enforcement:** OPA/Gatekeeper, Kyverno, IAM condition policies, API gateway policy.
- **Delivery plane:** GitHub Actions or GitLab CI, Argo CD / Flux.
- **Runtime controls:** EKS/AKS admission webhooks, network policies, service mesh policy, WAF.
- **Observability/evidence:** OpenTelemetry, SIEM (Splunk/Elastic), cloud audit logs.
- **Secrets/signing:** Vault, KMS, HSM-backed signing.

### Custom components (control-plane differentiators)
- **Authority Surface Manifest (ASM) service** for signed scope boundaries.
- **ENRICH gateway + Evidence Envelope service** for admissibility and anti-replay discipline.
- **Decision Record service** binding authority hash + policy hash + evidence references.
- **Consequence-tier controller** enforcing automation bounds by mission impact.
- **Replay ledger/index** for after-action reconstruction and audit-grade provenance.

## Reference production workload

**Workload archetype:** mission-support API + event processor + analytics store in Kubernetes, split across `mission-stage` and `mission-prod`.

- Data class: mixed operational + controlled mission metadata.
- Threat focus: identity abuse, supply-chain contamination, unauthorized data movement.
- Constraint: maintain availability while containing risk at machine tempo.

### Enforcement boundaries for this workload
- **Pipeline gate:** release promotion boundary.
- **Admission gate:** deployment/runtime boundary.
- **Segmentation gate:** network blast-radius boundary.
- **Identity gate:** privilege/token boundary.
- **Data gate:** access/egress boundary.

## Boundary contracts (ACP + CAF together)

### 1) Pipeline gate
- ACP checks principal trust scope for release action.
- CAF requires decision-grade release evidence (integrity, vulnerability posture, drift, confidence).
- Enforcement outcome: promote, hold, or deny via signed decision record.

### 2) Admission gate
- ACP validates deploy actor and policy compatibility.
- CAF checks live posture confidence and consequence-tier constraints.
- Enforcement outcome: admit, canary-only, or deny.

### 3) Segmentation gate
- ACP validates authority to change segmentation posture.
- CAF computes containment scope from active incident evidence.
- Enforcement outcome: isolate affected services, preserve mission-critical traffic paths.

### 4) Identity gate
- ACP enforces issuance/assumption rules for privileged identities.
- CAF tightens action eligibility as confidence degrades.
- Enforcement outcome: credential rotation, token narrowing, privilege reduction.

### 5) Data gate
- ACP enforces role-to-data policy compatibility.
- CAF applies active risk posture to data-access decisions.
- Enforcement outcome: deny or step-up controls for high-risk access paths.

## Live-fire scenario: production drift + privilege escalation attempt

### Situation
A production service begins making anomalous calls and attempts to assume a higher-privilege identity path. Simultaneously, a recent deployment introduces config drift in a network policy.

### Execution sequence
- **T+0 to T+5**
  - Evidence emitted from runtime telemetry, IAM audit events, and deployment controls.
  - ENRICH validates provenance/labels and opens incident work unit.

- **T+5 to T+15**
  - SCORE computes high-risk posture with sufficient confidence for containment.
  - SURFACE produces a bounded decision package: affected scope, consequence tier, allowed action set.

- **T+15 to T+30**
  - ACT executes through enforcement points:
    1) quarantine impacted workload segment,
    2) rotate credentials and constrain token minting,
    3) gate deployment promotion for impacted scope.

- **T+30 to T+60**
  - Independent verification confirms whether abuse path is closed and service objectives recover.
  - If not closed: automatic authority tightening and human-tier escalation.

- **T+60+**
  - Controlled rollback/forward recovery under decision-record discipline.
  - Replay package generated from evidence + decision + action chain.

## Operational quality metrics

- **MTTD2D:** mean time from detection to signed decision.
- **MTTBC:** mean time to bounded containment.
- **Decision binding rate:** % consequential actions with complete decision-record linkage.
- **Verification success rate:** % autonomous/assisted actions verified on first pass.
- **Escalation precision:** % tier escalations that were necessary (not noise).
- **Replay completeness:** ability to reconstruct exactly what was known/decided/done.

## Failure modes and hard guardrails

1. **Score becomes authority**
   - Guardrail: only signed manifest + policy grant authority.

2. **Unmediated automation side effects**
   - Guardrail: all consequential actions must traverse enforcement points.

3. **Evidence poisoning/replay**
   - Guardrail: ENRICH anti-replay + schema validation + quarantine pipeline.

4. **Containment breaks mission continuity**
   - Guardrail: consequence-tiered action sets + staged recovery verification.

5. **Policy drift between environments**
   - Guardrail: signed policy bundle version pinning + environment attestation checks.

## 90-day implementation sequence

### Days 0-30: foundation
- Stand up principal onboarding + workload identity discipline.
- Deploy ENRICH gateway minimum controls.
- Require signed decision records for at least one production pipeline gate.

### Days 31-60: bounded enforcement
- Extend enforcement to admission and segmentation boundaries.
- Activate consequence-tier policy constraints.
- Begin replay index for evidence and actions.

### Days 61-90: live-fire hardening
- Run a production-like live-fire exercise.
- Measure MTTD2D, MTTBC, verification success, and replay completeness.
- Tune quorum/outlier/escalation controls based on observed failure patterns.

## Expansion path to full paper

This draft should remain a working architecture note until we lock:
- canonical boundary contracts,
- baseline implementation profile,
- one full red-team/live-fire evidence chain.

Then expand into a full paper with deployment diagrams, conformance profiles, and a reference implementation appendix.

## Working abstract (paper candidate)

This paper operationalizes CAF-RA and ACP-RA as a unified production control-plane pattern for agentic enterprise operations. ACP defines enforceable authority for non-person principals and bounded action surfaces; CAF converts enterprise telemetry into decision-grade assurance through replayable evidence, confidence-bearing posture, and mediated enforcement. Using a reference mission-support workload, we show how authority, evidence, and execution are bound through signed decision records and verified outcomes at real change boundaries. The resulting architecture preserves governable control at machine tempo without sacrificing operational continuity.
