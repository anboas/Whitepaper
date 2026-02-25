---
title: "CAF + ACP in Production: Joint Deployment Playbook (Live-Fire Pattern)"
date: 2026-02-25
summary: "How CAF-RA and ACP-RA operate together in a real enterprise stack, including tooling map, custom control-plane components, and a live-fire production scenario."
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

## Why this note

CAF and ACP are strongest when presented together as one operating model:
- **ACP governs who/what can act** (identity, trust scopes, policy decisioning, tool-use boundaries).
- **CAF governs whether action is safe right now** (evidence, posture, confidence, bounded enforcement, verification).

Together they deliver machine-tempo execution without losing command authority.

## One-line thesis

**ACP decides action eligibility; CAF decides action advisability under current evidence; enforcement points execute bounded change; verification closes the loop.**

## Joint architecture spine (real-world)

1. **Identity + authority (ACP)**
   - Non-person principals (agents/services) onboarded with attributable identity.
   - Signed manifests + policy bundles define trust scopes and allowed action classes.

2. **Evidence pipeline (CAF)**
   - Runtime, pipeline, identity, and validation signals emitted as attributable evidence.
   - ENRICH gateway validates schema, labels handling boundaries, anti-replay checks, and tamper-evident anchoring.

3. **Decisioning (ACP + CAF)**
   - ACP policy decision point evaluates whether a requested action is authorized.
   - CAF SCORE computes posture + confidence from current evidence set.
   - Decision record binds policy hash + manifest hash + evidence references.

4. **Execution at boundaries (ACP-mediated, CAF-governed)**
   - Enforcement points at CI/CD gates, admission control, segmentation, identity issuance, data access, and bounded response automation.
   - Agents propose; enforcement points execute.

5. **Verification + replay (CAF)**
   - Independent verification confirms intended effect.
   - Action evidence closes loop for audit and after-action reconstruction.

## Tooling map (example production stack)

### Off-the-shelf stack
- **Identity/Auth:** Entra ID or Okta, workload identities, OIDC federation.
- **Policy/Enforcement:** OPA/Gatekeeper, Kyverno, IAM condition policies, API gateway policy.
- **Delivery plane:** GitHub Actions or GitLab CI, Argo CD / Flux.
- **Runtime controls:** EKS/AKS admission webhooks, network policies, service mesh policy, WAF.
- **Observability/evidence:** OpenTelemetry, SIEM (Splunk/Elastic), cloud audit logs.
- **Secrets/keys:** Vault / KMS / HSM-backed signing.

### Custom components (your differentiators)
- **Authority Surface Manifest (ASM) service** (signed, versioned trust scopes).
- **Evidence Envelope + ENRICH gateway** (schema, anti-replay, label discipline).
- **Decision Record service** binding policy + authority + evidence.
- **Consequence-tier controller** for bounded automation thresholds.
- **Replay ledger/index** for post-incident governance reconstruction.

## Example production workload (reference target)

**Workload archetype:** mission-support API + event processor + analytics store running in Kubernetes across two environments (mission-prod and mission-stage).

- **Data sensitivity:** mixed (operational telemetry + controlled mission metadata).
- **Blast-radius concern:** identity abuse, poisoned deployment, unauthorized data movement.
- **Operational requirement:** maintain service availability while enforcing containment at machine tempo.

### Practical control boundaries for this workload
- **Pipeline boundary:** block unsigned artifacts, failed policy checks, or missing decision records.
- **Admission boundary:** deny deploy when trust-scope or consequence-tier constraints are violated.
- **Network boundary:** isolate compromised workload segments via policy-based quarantine.
- **Identity boundary:** rotate/disable compromised credentials and constrain token issuance.
- **Data boundary:** enforce query/access controls and egress restrictions under incident posture.

## Boundary-by-boundary control contracts (ACP + CAF)

1. **Pipeline Gate**
   - ACP: validates principal + trust scope for proposed release action.
   - CAF: requires evidence package (build integrity, scan outputs, drift posture, confidence).
   - Enforcement: promote/deny with signed decision record.

2. **Admission Gate**
   - ACP: validates deployment actor and environment policy.
   - CAF: checks latest posture confidence and consequence-tier constraints.
   - Enforcement: admit, canary-only, or deny.

3. **Segmentation Gate**
   - ACP: validates authority for network policy changes.
   - CAF: uses incident evidence to determine containment scope.
   - Enforcement: isolate workloads, restrict east-west communication.

4. **Identity Gate**
   - ACP: enforces who can mint/assume privileged identities.
   - CAF: triggers tighter controls when confidence drops.
   - Enforcement: token restrictions, credential rotation, privilege reduction.

5. **Data Access Gate**
   - ACP: enforces role/data policy compatibility.
   - CAF: applies active posture constraints to dynamic access decisions.
   - Enforcement: deny/high-friction approvals for high-risk paths.

## Live-fire scenario (operational validation)

### Scenario: Production drift + suspicious privilege escalation in a mission-support workload

- **Trigger (EMIT/ENRICH):**
  Runtime detector flags anomalous pod behavior and IAM role misuse attempt. Signals sealed as evidence envelopes.

- **Assessment (SCORE):**
  CAF computes high-risk posture with degraded confidence in one service boundary; correlated evidence from independent producers raises confidence enough for containment.

- **Decision (SURFACE):**
  Decision work unit shows: affected service, blast radius estimate, allowed actions by consequence tier, and required approvals.

- **Action (ACT):**
  Under signed decision record, enforcement points:
  1) quarantine affected workload segment,
  2) rotate compromised credentials,
  3) gate further deployments touching impacted scope.

- **Verification (close loop):**
  Independent telemetry verifies exfil path shut, no new unauthorized role assumptions, service SLO restored.

### Why this matters operationally
- Containment starts in minutes, not days.
- Actions are bounded and attributable.
- Governance is preserved under stress.
- Post-incident replay is evidence-complete for command review.

## Live-fire execution timeline (operator runbook)

- **T+0 to T+5 min**
  - Detect anomaly, seal evidence, open incident work unit.
  - Auto-apply temporary consequence-tier elevation for affected scope.

- **T+5 to T+15 min**
  - Swarm/ensemble assessment confirms posture + confidence.
  - Generate signed decision record with bounded containment plan.

- **T+15 to T+30 min**
  - Enforcement points execute quarantine + credential controls.
  - Deploy pipeline for impacted scope moves to restricted mode.

- **T+30 to T+60 min**
  - Independent verification checks whether threat path is closed.
  - If failed: auto-tighten scope, reduce privileges further, escalate human approval tier.

- **T+60+**
  - Controlled recovery using decision-recorded rollback/forward actions.
  - After-action replay report generated directly from evidence + action records.

## Known failure modes and explicit guardrails

- **Failure mode:** “Model confidence masquerades as authority.”
  - **Guardrail:** authority only from signed manifest + policy, never from score output.

- **Failure mode:** unmediated automation side effects.
  - **Guardrail:** all consequential actions must traverse enforcement points under signed decision records.

- **Failure mode:** contaminated or replayed evidence influences posture.
  - **Guardrail:** ENRICH gateway signature checks, anti-replay fields, schema controls, quarantine path.

- **Failure mode:** containment succeeds but business continuity collapses.
  - **Guardrail:** consequence tiers + bounded action sets + staged recovery verification.

## Metrics that prove it works

- Mean time to detection-to-decision (MTTD2D)
- Mean time to bounded containment (MTTBC)
- % actions executed with complete decision record binding
- % autonomous actions that pass independent verification on first attempt
- Policy exception rate by consequence tier
- Replay completeness score (can we reconstruct exactly what happened?)

## Suggested publication path

1. Publish this as a **note first** (fast cycle, architecture + operations alignment support).
2. Expand into a **paper** with:
   - reference deployment diagrams,
   - control contracts per boundary,
   - one full red-team/live-fire walkthrough,
   - implementation profiles (core vs high-assurance).

## Suggested implementation sequence (90-day)

- **Days 0-30 (Foundations)**
  - Stand up identity-bound producer onboarding.
  - Implement ENRICH gateway minimum controls (schema, anti-replay, labeling).
  - Introduce signed decision records for one high-value pipeline gate.

- **Days 31-60 (Bounded enforcement)**
  - Expand enforcement points to admission + segmentation boundaries.
  - Add consequence-tier policy constraints and rollback discipline.
  - Enable replay ledger indexing for evidence + actions.

- **Days 61-90 (Operational hardening)**
  - Run live-fire exercise against a production-like workload.
  - Measure MTTD2D/MTTBC + verification pass rates.
  - Tune quorum/outlier and escalation policies from observed failures.

## Draft abstract for paper version

This paper operationalizes CAF-RA and ACP-RA as a unified production control-plane model for agentic enterprise operations. ACP defines enforceable authority for non-person principals and bounded tool use; CAF converts enterprise telemetry into decision-grade assurance through replayable evidence, confidence-bearing posture, and mediated enforcement. We present a deployable architecture using commodity enterprise tooling plus minimal custom control-plane components, and we validate the model against a live-fire production scenario. The result is a machine-tempo governance system where autonomous speed remains subordinate to explicit authority, bounded execution, and independent verification.
