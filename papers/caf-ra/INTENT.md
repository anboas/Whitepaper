# INTENT — Whitepaper Specification

> Single source of truth for what this paper is supposed to be.

## 0) Identity
- **Title:** Continuous Assurance Fabric Reference Architecture (CAF-RA)
- **Subtitle:** A control-plane architecture for governed, scalable continuous assurance at mission tempo
- **Author name:** Adam Boas
- **Author role:** Agentic Warfare Architect, Department of War
- **Date:** February 2026
- **Audience:** DoW CIO, platform owners, software factories, AO and security engineering teams
- **Distribution:** Unpublished draft (working paper)

## 1) Intent (what this paper does)
- Define CAF as a single governed loop: EMIT -> ENRICH -> SCORE -> SURFACE -> ACT.
- Make assurance decision-grade by binding authority artifacts, replayable evidence, and mediated enforcement.
- Provide a fieldable adoption path that preserves simplicity at the core and pushes complexity into profiles/patterns.

## 2) Definition of done (“polished”)
- Builds PDF/HTML in CI.
- Executive summary stays under 250 words.
- Normative technical positions are testable and map to real control boundaries.
- References tie CAF to ACP-RA, Code-as-Policy, and prior memo decisions.
- No TODO/TBD/FIXME markers.

## 3) Required sections
- Executive Summary
- Scope and Non-Goals
- Strategic Drivers
- Architectural Principles
- Core Vocabulary
- The CAF Loop (EMIT, ENRICH, SCORE, SURFACE, ACT)
- Governance Overlay
- Degraded-Mode and Federation
- Conformance Profiles and Patterns
- Adoption Path
- Conclusion
- References

## 4) Non-negotiables / constraints
- Tone: direct, policy-technical, implementation grounded.
- Keep the mental model simple; avoid ontology sprawl.
- Keep authority separate from context and scoring.
- Use Department of War (DoW) naming convention.

## 5) Notes / source material
- Source seed: inbound draft `file_153---25b7f715-82d8-41bb-b67c-11a30ad793e6.txt`.
- Related references:
  - ACP-RA paper
  - DAD memo
  - Code-as-Policy paper
  - Agentic Force Creation paper
- Source of truth for this paper: `papers/caf-ra/tex/paper.tex`

## 6) Assets (optional)
- none yet

## 7) Requirements (optional)
- none
