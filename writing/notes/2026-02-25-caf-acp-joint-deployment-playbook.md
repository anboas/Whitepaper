---
title: "CAF + ACP Joint Deployment: Production Reference Pattern"
date: 2026-02-25
summary: "A reference-grade deployment pattern for running CAF-RA and ACP-RA together in real production systems, with concrete tooling, control contracts, and a live-fire workload scenario."
status: draft
type: note
tags:
  - caf-ra
  - acp-ra
  - reference-architecture
  - deployment
  - production
  - control-planes
  - governance
  - continuous-assurance
---

## 1. Problem statement

Modern enterprises already operate at machine tempo. CI pipelines promote code continuously, identities are minted and exchanged by services, and agents can now propose and trigger meaningful side effects. The operating reality is not "occasional change". It is persistent change under uncertainty.

Most governance models fail here in one of two ways:

1. **Policy theater**: evidence and dashboards exist, but they do not constrain real execution boundaries.
2. **Approval drag**: controls are bolted into human workflow, so velocity and safety are forced into tradeoff.

CAF + ACP exists to remove that tradeoff.

## 2. Core thesis

**ACP governs action eligibility. CAF governs action advisability under current evidence and confidence. Enforcement points execute bounded effects. Verification closes the loop.**

That is the joint spine.

## 3. Architectural intent

This pattern defines how to make autonomous and semi-autonomous operations:

- fast enough for production tempo,
- governable under adversarial conditions,
- reconstructable after incident or mission degradation.

The target condition is not a perfect prevention system. The target condition is a control system where:

- authority remains explicit,
- evidence remains replayable,
- consequential actions remain bounded and attributable.

## 4. Scope and non-goals

### In scope
- Runtime production environments (Kubernetes + cloud-managed services)
- CI/CD promotion and admission boundaries
- Identity, network, and data-access control boundaries
- Agent-assisted triage and bounded remediation

### Not in scope
- Single-vendor implementation lock-in
- Full ontology expansion beyond CAF/ACP core contracts
- Replacing command authority with automated confidence outputs

## 5. Joint model: two planes, one doctrine

### Plane A: Authority and action governance (ACP)
ACP defines who or what may act, where, and within which bounded scope:

- non-person principals with attributable identity
- trust scopes
- signed authority manifests
- signed policy bundles
- mediated action/tool surfaces

### Plane B: Continuous assurance and bounded execution (CAF)
CAF defines whether action should proceed now, under current posture and confidence:

- EMIT and ENRICH evidence discipline
- SCORE with confidence-bearing posture
- SURFACE as supervised decision work
- ACT through mediated enforcement points
- independent verification and replay

### Seam rule
ACP without CAF authorizes actions that may be operationally unwise under degraded evidence. CAF without ACP assesses risk but cannot enforce authority discipline. Joint operation is mandatory for machine-tempo governance.

## 6. Loop contract (production form)

### EMIT
- **Question**: what changed, and who is asserting it?
- **Output**: attributable, sealable evidence claims
- **Failure mode**: anonymous/spoofed producer influence
- **Primary control**: principal onboarding + producer identity discipline

### ENRICH
- **Question**: is evidence admissible, transportable, and replay-safe?
- **Output**: normalized, labeled, anti-replay-validated envelopes
- **Failure mode**: poisoned/replayed/mislabeled inputs entering governance
- **Primary control**: governed ingestion gateway with quarantine path

### SCORE
- **Question**: what is posture now, and how certain are we?
- **Output**: confidence-bearing posture claims with trace to evidence IDs
- **Failure mode**: opaque score interpreted as authority
- **Primary control**: explainability + authority/data separation

### SURFACE
- **Question**: what decision is pending, under what authority, with what evidence?
- **Output**: supervised assurance work units
- **Failure mode**: dashboard theater or operator bypass
- **Primary control**: decision surfaces with explicit provenance and decision records

### ACT
- **Question**: what bounded action is eligible now?
- **Output**: mediated action evidence tied to signed decision record
- **Failure mode**: unmediated side effects / runaway remediation
- **Primary control**: enforcement points + consequence-tier constraints + verification closure

## 7. Production reference workload

### Workload archetype
A mission-support service set:

- API tier (mission workflow control)
- event processor (high-volume ingest)
- analytics/data store (controlled mission metadata)
- deployed across `mission-stage` and `mission-prod`

### Operational constraints
- maintain service availability under containment
- prevent identity escalation becoming lateral movement
- prevent unapproved data movement under incident posture

### High-value boundaries
- pipeline promotion boundary
- runtime admission boundary
- network segmentation boundary
- identity issuance/assumption boundary
- data-access + egress boundary

## 8. Tooling blueprint (real-world stack)

### Commodity components
- **Identity/Auth**: Entra ID or Okta, workload identity federation, OIDC
- **Policy enforcement**: OPA/Gatekeeper, Kyverno, IAM conditions, API gateway policy
- **Delivery**: GitHub Actions or GitLab CI, Argo CD / Flux
- **Runtime controls**: admission webhooks, network policy, service mesh authz, WAF
- **Telemetry**: OpenTelemetry, SIEM (Elastic/Splunk), cloud audit trails
- **Cryptographic roots**: Vault/KMS/HSM-backed signing

### Control-plane differentiators (custom)
- **ASM Service**: signed authority and trust-scope publication
- **ENRICH Gateway + Envelope Service**: schema/label/replay control point
- **Decision Record Service**: policy hash + manifest hash + evidence binding
- **Consequence-Tier Controller**: explicit runtime action constraints by mission impact
- **Replay Ledger/Index**: deterministic after-action reconstruction

## 9. Boundary contracts (ACP + CAF together)

### 9.1 Pipeline gate
- ACP validates principal trust scope for release action.
- CAF requires decision-grade release evidence package.
- Enforcement outcome: promote / hold / deny under signed decision record.

### 9.2 Admission gate
- ACP validates deployment actor and environment compatibility.
- CAF checks current posture confidence and tier constraints.
- Enforcement outcome: admit / canary / deny.

### 9.3 Segmentation gate
- ACP validates authority for segmentation control changes.
- CAF computes required containment scope from active evidence.
- Enforcement outcome: isolate impacted services while preserving critical mission paths.

### 9.4 Identity gate
- ACP enforces token issuance and privileged assumption constraints.
- CAF tightens eligibility as confidence drops or adverse signals increase.
- Enforcement outcome: rotate credentials, narrow token claims, reduce privileges.

### 9.5 Data gate
- ACP enforces role/data-policy compatibility and allowed action class.
- CAF applies current risk posture to dynamic access and egress decisions.
- Enforcement outcome: deny, constrain, or step-up control path.

## 10. Live-fire scenario (production)

### Trigger condition
A production service begins anomalous outbound behavior and attempts privileged identity escalation shortly after a deployment introducing segmentation drift.

### Sequence

- **T+0 to T+5**
  - Runtime and IAM events emitted and sealed.
  - ENRICH validates admissibility and opens incident work unit.

- **T+5 to T+15**
  - SCORE converges on high-risk posture with adequate confidence for containment.
  - SURFACE issues bounded decision package with tier, scope, and allowed actions.

- **T+15 to T+30**
  - ACT executes through enforcement points:
    1) workload segment quarantine,
    2) credential/token control action,
    3) pipeline promotion restrictions for impacted scope.

- **T+30 to T+60**
  - Independent verification tests whether abuse path is actually closed.
  - If not closed: automatic authority tightening and escalation tier increase.

- **T+60+**
  - Controlled recovery under decision-record discipline.
  - Replay package generated for operational and governance review.

## 11. Quality metrics (operational proof)

- **MTTD2D**: mean time from detection to signed decision
- **MTTBC**: mean time to bounded containment
- **Decision-binding coverage**: % consequential actions with complete decision linkage
- **Verification first-pass rate**: % actions verified without corrective re-run
- **Escalation precision**: % escalations later validated as necessary
- **Replay completeness**: ability to reconstruct event chain without narrative gaps

## 12. Failure taxonomy and hard guardrails

1. **Score as authority**
   - Guardrail: authority only from signed manifests + policy bundles.

2. **Unmediated side effects**
   - Guardrail: all consequential effects traverse enforcement points under signed decision record.

3. **Evidence poisoning/replay**
   - Guardrail: ENRICH schema/label/anti-replay controls + quarantine path.

4. **Containment overreach causing mission outage**
   - Guardrail: tier-bounded action sets + staged verification + controlled recovery path.

5. **Cross-environment policy drift**
   - Guardrail: signed bundle pinning + environment attestation checks at boundaries.

## 13. 90-day implementation path

### Days 0-30: foundation
- enforce principal onboarding for evidence producers and effectors
- deploy ENRICH gateway baseline controls
- require signed decision records on one production pipeline gate

### Days 31-60: bounded enforcement
- extend enforcement to admission and segmentation boundaries
- activate consequence-tier controller for runtime action eligibility
- enable replay indexing for evidence and action records

### Days 61-90: operational hardening
- run live-fire against production-like workload
- measure core tempo/quality metrics
- tune quorum, escalation, and outlier treatment from observed failures

## 14. Conformance levels (for scaling)

- **Level 1 (Foundational)**: identity discipline + enriched evidence + decision records at pipeline boundary
- **Level 2 (Operational)**: admission/segmentation enforcement + consequence-tier constraints + replay closure
- **Level 3 (High-assurance)**: broad boundary coverage, independent verification rigor, rehearsed degraded-mode operations

## 15. Expansion path to full paper

This note should remain draft until we lock:

- canonical boundary contracts,
- at least one validated live-fire evidence chain,
- baseline conformance profile definitions.

Then expand into paper form with:
- architectural views and sequence diagrams,
- implementation profiles and deployment variants,
- after-action evidence appendix,
- conformance checklist and measurable criteria.

## Working abstract (paper candidate)

This paper operationalizes CAF-RA and ACP-RA as a unified production control-plane pattern for agentic enterprise operations. ACP defines enforceable authority for non-person principals and bounded action surfaces; CAF converts enterprise telemetry into decision-grade assurance through replayable evidence, confidence-bearing posture, and mediated enforcement. Using a reference mission-support workload, we show how authority, evidence, and execution are bound through signed decision records and independent verification at real change boundaries. The resulting architecture preserves governable control at machine tempo without sacrificing operational continuity.
