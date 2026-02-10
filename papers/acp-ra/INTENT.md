# INTENT — Whitepaper Specification

> Single source of truth for what this paper is supposed to be.

## 0) Identity
- **Title:** Agent Control Plane Reference Architecture (ACP-RA)
- **Subtitle:** Governed, scalable agentic autonomy for contested and degraded operations
- **Author name:** Adam Boas
- **Author role:** (fill)
- **Date:** 2026-02-10
- **Audience:** DoW CIO / enterprise architects / platform teams / operators
- **Distribution:** adamboas.info (paper) + derivative memo threads

## 1) Intent (what this paper does)
- Provide a DoW CIO–style reference architecture for governed autonomy.
- Define stable primitives (NPE identity, trust scopes, work units, gateways, evidence) that constrain downstream implementations.
- Translate “agent capability” into enforceable controls aligned to Zero Trust, ICAM, CNAP, DevSecOps, and cATO.

## 2) Definition of done (“polished”)
- Builds PDF/HTML in CI.
- Executive summary < 250 words.
- Technical positions are testable and map to concrete control surfaces.
- Includes citations/links for DoW CIO references + industry interop protocols.
- No TODO/TBD/FIXME.

## 3) Required sections
- Executive Summary
- Scope and Non-Goals
- Strategic Drivers
- Architectural Principles
- Vocabulary
- Consequence Tiers
- Technical Positions (required control surfaces)
- Architecture Components
- Control Loops
- Multi-Agent Governance
- Contested/Degraded Operation
- Patterns
- Metrics + Roadmap
- References

## 4) Non-negotiables / constraints
- Tone: crisp, DoW CIO reference architecture style.
- Avoid vendor lock-in; protocol-neutral.
- Explicitly exclude use-of-force guidance; cite DoWD 3000.09.

## 5) Notes / source material
- Source of truth: `tex/paper.tex` in this folder. (`draft.md` is optional/legacy; do not treat it as authoritative.)

## 6) Assets (optional)
- `diagrams/` for OV-1 and loop diagrams (PNG).

## 7) Requirements (optional)
- N/A
