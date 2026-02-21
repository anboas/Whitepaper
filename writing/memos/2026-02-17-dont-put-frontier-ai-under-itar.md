---
title: "Don't Put Frontier AI Under ITAR: A Blunt Instrument for a Dual-Use Reality"
date: 2026-02-17
summary: "A policy memo arguing against sweeping ITAR treatment for frontier AI and proposing a targeted control framework centered on narrow export controls, defense-unique controls, and enforceable operational provenance."
status: draft
type: memo
pdfPath: /memos/2026-02-17-dont-put-frontier-ai-under-itar.pdf
tags:
  - ai-policy
  - export-controls
  - itar
  - frontier-ai
  - governance
---

## Executive Recommendation

Do not place general-purpose frontier artificial intelligence (AI) development under the International Traffic in Arms Regulations (ITAR).

Instead, adopt a three-part policy:

1. Keep broad frontier model development under the Export Administration Regulations (EAR), with narrow controls on specific high-risk artifacts and chokepoints.
2. Apply ITAR only to defense-unique implementations and services designed for military end use.
3. Require enforceable operational provenance for high-consequence agentic systems: clear identity, explicit authorization, and replayable action evidence.

This approach is stronger in practice because it constrains real risk surfaces without freezing the U.S. innovation base.

## Why Sweeping ITAR Coverage Is the Wrong Tool

The argument for full ITAR treatment sounds simple: advanced models can support lethal autonomy, cyber operations, and strategic influence, so regulate frontier AI like munitions.

The problem is that ITAR was built for defense articles, defense services, and associated technical data on the U.S. Munitions List [1]. ITAR can be expansive by design, including treatment of disclosures to foreign persons as exports in defined contexts [2]. That design is appropriate for missiles, targeting systems, and tightly bounded military technologies. It is poorly matched to a distributed software ecosystem where capability is produced by combinations of model weights, data pipelines, evaluations, compute access, and operations engineering.

If policymakers "ITARize" general frontier AI development, the primary effect will be operational drag inside U.S. teams, not durable denial of capability abroad.

### 1) It would tax routine engineering and collaboration

Modern AI work depends on cross-border teams, external researchers, cloud operators, and security responders. Sweeping ITAR treatment would push normal workflows into compliance-heavy pathways, slowing development and incident response.

### 2) It would concentrate innovation in a few incumbents

Large firms can absorb complex export-control overhead. Startups, university labs, and smaller dual-use companies generally cannot. That creates policy-induced concentration risk.

### 3) It would not stop capable actors from building abroad

Advanced AI capability is already global. Aggressive U.S. restrictions can slow selected transfers, but they also incentivize offshore substitutes and sovereign programs. A maximalist framework can isolate U.S. participation faster than it suppresses global capability growth.

## Evidence From Recent Export-Control Friction

Recent policy movement already shows the difficulty of broad diffusion controls. In 2025, the Bureau of Industry and Security (BIS) rescinded the prior AI Diffusion Rule and stated intent to replace it with a different approach [3].

That episode does not prove export controls are ineffective. It does show that over-broad controls can trigger strategic and operational backlash, even before moving to the higher-friction ITAR regime.

Congressional Research Service (CRS) analysis has also highlighted how advanced-compute and model-related controls are tied to specific technical chokepoints, not a blanket prohibition on all AI development [4]. That supports a narrow-control strategy rather than a category-wide ITAR shift.

## What to Control Instead

The central policy mistake is framing the problem as "AI exists" instead of "AI acts in high-consequence environments without enforceable governance."

For national security risk management, the key control points are operational:

- who is acting,
- with what delegated authority,
- against which systems and data,
- under what policy gates,
- with what auditable evidence.

This is where architecture and enforcement matter. A control-plane model, such as the Agent Control Plane Reference Architecture (ACP-RA), addresses those conditions directly through delegated authority boundaries, policy decision points, and provenance requirements [5].

## Target Policy Package

A publishable U.S. position can be both hard-edged and practical:

1. **EAR-first for general frontier AI:** keep baseline model development and broad commercial research in EAR scope, with technical thresholding tied to identifiable risk artifacts.
2. **ITAR for defense-unique implementations:** apply ITAR when systems, fine-tunes, integrations, or services are purpose-built for military targeting, weapons employment, mission-system integration, or equivalent defense-unique end use.
3. **Mandatory provenance in high-consequence deployments:** require identity-bound delegation, policy-gated tool execution, immutable logs, and replayable evidence for regulated mission environments.
4. **Periodic threshold review:** update controlled-artifact definitions on a fixed cadence so controls remain tied to real technical change, not static assumptions.

## Bottom Line

A sweeping ITAR approach to frontier AI feels forceful but is strategically blunt. It risks slowing U.S. innovation and allied collaboration while delivering limited long-run denial of capability to determined external actors.

A stronger strategy is targeted export control plus enforceable operational governance.

Control what is genuinely defense-unique. Control the chokepoints that are technically meaningful. And require verifiable identity, authorization, and provenance where autonomous systems can produce real-world effects.

## References

1. Electronic Code of Federal Regulations (eCFR), 22 CFR Parts 120-121 (ITAR scope, definitions, and U.S. Munitions List structure). https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M
2. Cornell Law School Legal Information Institute, International Traffic in Arms Regulations (ITAR) overview (including deemed-export framing). https://www.law.cornell.edu/wex/international_traffic_in_arms_regulations_%28itar%29
3. Bureau of Industry and Security (BIS), U.S. Department of Commerce, "Department of Commerce Announces Rescission of Biden-Era Artificial Intelligence Diffusion Rule." https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens
4. Congressional Research Service (CRS), "U.S. Export Controls and China: Advanced Semiconductors" (R48642), including discussion of AI-related control direction and chokepoint strategy. https://www.congress.gov/crs-product/R48642
5. Adam Boas, "Agent Control Plane Reference Architecture (ACP-RA)." https://www.adamboas.com/writing/acp-ra/
