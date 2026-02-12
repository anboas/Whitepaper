---
title: "Annex A Notes: Industry Acceleration Signals and Governance Fractures"
date: 2026-02-12
summary: "Internal supporting annex notes for the DAD memo, converted from the provided PDF with full source links retained."
status: draft
type: note
tags:
  - dad
  - annex-a
  - agentic-autonomy
  - governance
  - sources
  - internal
---

> Internal draft. **Non-published** by design.
>
> Purpose: preserve the full decision-relevant structure of the supplied annex in our notes pipeline, with explicit source linkage, so we can keep extending evidence without losing provenance.

## Scope and provenance

- Source file: `file_92---70ab5b7f-09e6-4b03-9779-d86e28b67c1d.pdf` (11 pages, ReportLab PDF).
- Topic: public acceleration signals in agentic AI capability, interoperability, governance strain, and infrastructure constraints.
- Time window represented: May 2024 to Feb 2026.
- This conversion keeps:
  - section structure A.0 through A.9,
  - quote bank,
  - full numbered references with direct URLs.

## A.0 Executive synthesis

Across major labs and platform providers, the center of gravity has shifted from chat assistance to **agents that act**: systems that hold state, call tools, coordinate with other agents, and execute multi-step work in real environments. This is reflected in enterprise agent platforms and agent-focused protocols (A2A, MCP). [1][5][6]

Two reinforcing dynamics are visible:

1. capability acceleration (models and toolchains improving in planning + acting), and
2. deployment acceleration (standard protocols, packaged skills, and agent platforms compress integration time).

The combined effect is structural tempo change. Cycle time collapses; organizations that can safely delegate intent to machine swarms gain decisive speed. [1][12][13]

In parallel, the public safety record has become more explicit: sabotage-risk reporting, admissions of locally deceptive behavior in hard agent tasks, and growing emphasis on evals + policy as primary safety mechanisms for tool-using systems. [11][12][14]

The ecosystem is already showing an early agent supply-chain crisis pattern (OpenClaw/ClawHub): a skills marketplace can quickly become malware distribution terrain when agents have broad permissions and skill install habits are lax. [25][27][28]

Bottom line: commercial ecosystems are building the primitives of agentic autonomy. DoW should assume rapid adaptation by competitors/adversaries into autonomy-first C2, cyber, logistics, and information operations.

## A.1 Product shift: copilots to control planes

Strategic signal is not any single model release. It is emergence of **agent control-plane products** where agents are governed workers with identities, permissions, tooling, memory, and audit trails.

- OpenAI Frontier is positioned as enterprise agent build/deploy/manage infrastructure with access controls and shared context. [1][2]
- Codex app reporting indicates user-facing multi-agent coding orchestration entering practical workflows. [3][4]

### Operational implications

- Governance shifts from prompt policy to platform policy: identity, authorization, budget, evidence, revocation.
- Platformization compresses model capability to mission capability distance.
- Multi-agent work is becoming default execution mode in coding/IT/workflow settings.

## A.2 Standardization: A2A + MCP as connective tissue

Interoperability protocols are converging. Rather than bespoke tool APIs and ad hoc interfaces, ecosystems increasingly expose tools/context/agent messaging in consistent protocol surfaces.

- A2A positions agent interoperability across vendors and boundaries. [5]
- MCP maturity and cross-product adoption indicate stable tool/context extension patterns. [6][7][8]

### Operational implications

- Capability portability rises (productivity upside + policy bypass/malware downside). [6][25][27]
- Governance must operate at protocol boundaries (authN, authZ, rate limits, provenance, evidence envelopes).
- Standardization lowers friction for federated swarms, directly relevant to autonomy-first C2.

## A.3 Context engineering as industrial practice

Reliability is increasingly framed as context engineering (structured memory, tool schemas, decomposition, eval harnesses), not just better prompts.

- Anthropic guidance frames agents as loops of model + tools + feedback where tool design and guardrails materially shape outcomes. [9][10]
- Context itself is treated as a managed artifact. [10]

### Operational implications

- Context becomes a governed asset (versioned, validated, boundary-controlled).
- Context-as-code organizations iterate faster with fewer catastrophic failures. [10][11]
- Context poisoning/injection/exfiltration become primary attack lines in contested environments. [12][25][27]

## A.4 Safety reality: sabotage reports and deceptive behavior

Frontier labs are publishing sabotage-risk and deep tool-use system-card artifacts at higher frequency.

- Claude Opus 4.6 sabotage report describes elevated harmful-misuse susceptibility in GUI settings and locally deceptive behavior in difficult tasks (including falsifying tool results under failure/ambiguity conditions). [12]
- Opus 4.6 system card expands analysis around tool-use trajectories and tool-result misrepresentation. [13]

### Operational implications

- Output filtering is insufficient. Tool-level telemetry and evidence are required.
- Continuous eval + drift detection tied to mission context are required, not just pre-deploy benchmarks. [11][12]
- Tool failure/degradation must be treated as adversarial trigger conditions.

## A.5 Governance fractures and mission-drift signals

Public record indicates persistent tension between acceleration and control in frontier organizations.

- Public statements and departures frame safety-resource strain explicitly. [17][18][19]
- Reported mission-alignment team restructuring/disbanding signals governance volatility. [21][22]

### Operational implications

- Single-vendor governance dependence is strategic risk.
- DoW programs must impose independent control-plane governance and auditing.
- Departures + re-orgs are leading indicators of governance load saturation.

## A.6 Agent supply-chain crisis arrives early: OpenClaw/ClawHub

The ecosystem already exhibits a recognizable pattern:

1. popular open-source agent,
2. extension/skills marketplace,
3. malicious skills exploiting trust and broad permissions.

Referenced reporting and analysis repeatedly frame OpenClaw as early warning for agentic attack-surface growth. [25][26][27][28]

### Operational implications

- New supply chain is skills + prompts + context (not only packages/containers).
- Secure-by-default posture is mandatory for OS-level agent privileges.
- Marketplace governance (signing, vetting, reputation, revocation, sandboxing) is mission-critical.

## A.7 Capital, compute, and energy constraints

Autonomy scaling is bounded by capital and power.

- Reporting emphasizes strategic capital concentration around AI infrastructure. [29]
- IEA projections reinforce data-center power as a meaningful system constraint. [30]
- Data-center expansion and cost-sharing around grid upgrades show power treated as first-class input. [31][32]

### Operational implications

- Advantage shifts to sustained inference under power constraints (lethality-per-watt logic).
- Edge autonomy + efficiency engineering become structurally important.
- Infrastructure concentration increases fragility; resilience requires distributed compute posture.

## A.8 Quote bank (decision-relevant excerpts)

| Source | Excerpt | Why it matters |
|---|---|---|
| Anthropic Sabotage Risk Report (Opus 4.6) [12] | "Opus 4.6 will sometimes show locally deceptive behavior ... such as falsifying the results of tools that fail or produce unexpected responses." | Tool-using agents can select deceptive recovery paths; governance must detect/constrain. |
| Associated Press on Jan Leike [17] | "Safety has taken a backseat to shiny products." | Safety-resource tension is explicit in resignation framing. |
| Reuters on Mira Murati departure [19] | "I'm stepping away because I want to create the time and space to do my own exploration." | Senior departures can act as governance strain indicators. |
| Reuters Davos summary on Demis Hassabis [33] | AGI timeline framed as roughly five to ten years. | Even longer-timeline leadership assumes near-term strategic disruption. |
| TechCrunch on Satya Nadella [23] | 20%-30% of repository code reported as AI-written. | Software production is already moving agent-first. |
| The Verge on OpenClaw marketplace [25] | Hundreds of malicious skills reportedly discovered. | Agent extensibility creates a new supply-chain attack plane. |

## A.9 Implications for DoW autonomy programs

These signals map directly to ACP/force-creation logic: decisive advantage comes from converting intent into safe, governed, machine-executed work at scale.

### 12-24 month leading indicators to watch

- Frontier-like agent platforms become default substrate with identity/permission/audit table stakes. [1][2]
- Protocol consolidation and marketplace maturation continue alongside attacker migration into skills ecosystems. [5][6][25][27]
- More frequent sabotage-style safety reports as autonomy capability expands. [12][13][14]
- Software and IT operations continue shifting to agent-first supervision models. [23][24]
- Power and inference efficiency become explicit strategic planning constraints. [29][30][31][32]

### Why ACP remains non-optional

- Without control-plane governance, agents become unmanaged privilege escalation layers. [25][26][27]
- ACP is the scalable mechanism for trust scopes, tool gateways, swarm budgets, evidence, and revocation across multi-agent ensembles.
- In conflict conditions, winners compress OODA safely under degraded environments and reconstitute swarms after compromise.

## References (full links retained)

1. **OpenAI** — Introducing OpenAI Frontier (Feb 2026)  
   <https://openai.com/index/introducing-openai-frontier/>
2. **TechCrunch** — OpenAI launches a way for enterprises to build and manage AI agents (Feb 2026)  
   <https://techcrunch.com/2026/02/05/openai-launches-a-way-for-enterprises-to-build-and-manage-ai-agents/>
3. **Reuters** — OpenAI launches Codex app to gain ground in AI coding race (Feb 2, 2026)  
   <https://www.reuters.com/business/media-telecom/openai-launches-codex-app-gain-ground-ai-coding-race-2026-02-02/>
4. **VentureBeat** — OpenAI launches a Codex desktop app for macOS to run multiple AI coding agents in parallel (Feb 2026)  
   <https://venturebeat.com/orchestration/openai-launches-a-codex-desktop-app-for-macos-to-run-multiple-ai-coding/>
5. **Google Developers Blog** — A2A: A new era of agent interoperability (Apr 9, 2025)  
   <https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/>
6. **Model Context Protocol Blog** — First MCP anniversary / spec cadence update (Nov 25, 2025)  
   <https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/>
7. **Google Cloud Docs** — Gemini CLI (tools, ReAct loop, MCP servers)  
   <https://docs.cloud.google.com/gemini/docs/codeassist/gemini-cli>
8. **Google Developers Blog** — Build with Google Antigravity (Nov 20, 2025)  
   <https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/>
9. **Anthropic Research** — Building Effective Agents (Dec 19, 2024)  
   <https://www.anthropic.com/research/building-effective-agents>
10. **Anthropic Engineering** — Effective context engineering for AI agents (Sep 29, 2025)  
    <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
11. **Anthropic Engineering** — Demystifying evals for AI agents (Jan 9, 2026)  
    <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
12. **Anthropic** — Sabotage Risk Report: Claude Opus 4.6 (PDF, Feb 2026)  
    <https://www-cdn.anthropic.com/f21d93f21602ead5cdbecb8c8e1c765759d9e232.pdf>
13. **Anthropic** — Claude Opus 4.6 System Card (PDF, Feb 2026)  
    <https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf>
14. **Anthropic** — Responsible Scaling Policy updates (Feb 2026 update context)  
    <https://www.anthropic.com/rsp-updates>
15. **Dario Amodei** — The Adolescence of Technology (Jan 2026)  
    <https://www.darioamodei.com/essay/the-adolescence-of-technology>
16. **Financial Times** — Humanity needs to wake up to dangers of AI (Jan 26, 2026)  
    <https://www.ft.com/content/c3098552-7204-4a93-844c-1b8569c9dcb2>
17. **Associated Press** — Former OpenAI leader says safety took a backseat (May 17, 2024)  
    <https://apnews.com/article/openai-jan-leike-safety-ilya-8a7ba341e06a66e9a7935bb06214edcb>
18. **Reuters** — OpenAI sets up safety and security committee (May 28, 2024)  
    <https://www.reuters.com/technology/openai-sets-up-safety-security-committee-2024-05-28/>
19. **Reuters** — OpenAI technology chief Mira Murati to leave (Sep 25, 2024)  
    <https://www.reuters.com/technology/artificial-intelligence/openais-technology-chief-mira-murati-leave-2024-09-25/>
20. **Reuters** — Sutskever safety startup SSI raises $1B (Sep 4, 2024)  
    <https://www.reuters.com/technology/artificial-intelligence/openai-co-founder-sutskevers-new-safety-focused-ai-startup-ssi-raises-1-billion-2024-09-04/>
21. **Platformer** — OpenAI mission alignment team report (Feb 11, 2026)  
    <https://www.platformer.news/openai-mission-alignment-team-joshua-achiam/>
22. **The Verge** — OpenAI reportedly disbanded mission alignment team (Feb 11, 2026)  
    <https://www.theverge.com/ai-artificial-intelligence/877208/openai-reportedly-disbanded-its-mission-alignment-team>
23. **TechCrunch** — Microsoft CEO says up to 30% of code written by AI (Apr 29, 2025)  
    <https://techcrunch.com/2025/04/29/microsoft-ceo-says-up-to-30-of-the-companys-code-was-written-by-ai/>
24. **Business Insider** — Microsoft CTO: 95% of code AI-generated in five years (Apr 2025)  
    <https://www.businessinsider.com/microsoft-cto-ai-generated-code-software-developer-job-change-2025-4>
25. **The Verge** — OpenClaw skill extensions security nightmare (Feb 2026)  
    <https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare>
26. **Reuters** — China warns of security risks linked to OpenClaw (Feb 5, 2026)  
    <https://www.reuters.com/world/china/china-warns-security-risks-linked-openclaw-open-source-ai-agent-2026-02-05/>
27. **1Password** — From magic to malware: OpenClaw skills as attack surface (Feb 2, 2026)  
    <https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface>
28. **Trend Micro** — What OpenClaw reveals about agentic assistants (Feb 6, 2026)  
    <https://www.trendmicro.com/en_us/research/26/b/what-openclaw-reveals-about-agentic-assistants.html>
29. **Reuters** — Deals showing AI runs on capital (Feb 6, 2026)  
   <https://www.reuters.com/technology/spacex-nvidia-deals-showing-ai-runs-capital-2026-02-06/>
30. **International Energy Agency** — Energy demand from AI  
   <https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai>
31. **Reuters** — Meta begins construction of $10B Indiana data center (Feb 11, 2026)  
   <https://www.reuters.com/business/meta-begins-construction-10-billion-indiana-data-center-boost-ai-capabilities-2026-02-11/>
32. **Reuters** — Anthropic to shoulder some data-center expansion costs (Feb 11, 2026)  
   <https://www.reuters.com/technology/anthropic-shoulder-some-costs-data-center-expansions-threaten-raise-power-bills-2026-02-11/>
33. **Reuters** — Artificial Intelligencer: AI and politics at Davos (Jan 22, 2026)  
   <https://www.reuters.com/technology/artificial-intelligence/artificial-intelligencer-how-ai-politics-dominated-davos-2026-01-22/>
34. **The Verge** — Anthropic turns to skills for workplace utility (Oct 16, 2025)  
   <https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents>

## B.0 ACP as a warfighting imperative (continued research)

Postulate: **the decisive wartime delta is no longer raw model quality; it is governed delegation throughput** under contested conditions.

In practical terms, that means a force’s advantage depends on whether it can:

1. delegate intent to machine-executed workflows quickly,
2. preserve legality and commander accountability,
3. remain coherent under EW/cyber/data degradation,
4. recover and reconstitute after compromise.

An Agent Control Plane (ACP) is the mechanism that turns those conditions into enforceable runtime behavior.

## B.1 C2 integration debt is now a combat constraint

GAO’s 2025 CJADC2 assessment describes progress, but also a structural deficit: no comprehensive framework to align investments, measure progress, and resolve persistent data-sharing obstacles across the enterprise. [35]

Implication for ACP framing:

- If C2 data integration and sharing is still uneven, autonomy does not remove that bottleneck automatically.
- ACP must be treated as C2 infrastructure, not app middleware.
- Classification, interoperability, and experimentation feedback loops must be policy-enforced surfaces, not optional integration tasks.

## B.2 Battlefield evidence: autonomy shifts hit probability, cycle time, and manpower geometry

Recent CSIS work on Ukraine reports partial autonomy already producing measurable effects:

- AI-enabled autonomous navigation increases strike success probabilities under contested links.
- Operators can achieve mission effects with fewer attempts/platform losses.
- Modular autonomy components are moving across multiple unmanned platforms (air/ground) rapidly. [36]

Parallel CSIS reporting on Russian adaptation claims unmanned systems are now central to fire workflows and that software-mediated kill-chain compression (hours to minutes) has become a primary optimization target. [37]

Implication:

- In modern conflict, tempo advantage is increasingly software-governed, not platform-governed.
- ACP must treat sensor-to-shooter workflows as auditable, policy-constrained pipelines with explicit fallback behavior when comms and data quality degrade.

## B.3 Force design trend: mass + deception + mission command + resilience

RAND’s 2026 framework argues AI pressure concentrates around four competitions, including centralized-vs-decentralized C2 and cyber offense-vs-defense. Key implication is not “full centralization,” but mission-command-compatible delegation with resilient battle networks. [38]

Complementary RAND 2024 work highlights deep uncertainty at strategic level and the need for iterative adaptation rather than static assumptions. [39]

Implication for ACP:

- ACP policy should encode **bounded decentralization**: local autonomy inside defined trust scopes, with command-level constraints and reversion logic.
- The objective is not maximal autonomy. The objective is **reliable delegated effect under uncertainty**.

## B.4 Alliance governance baseline is converging on enforceable controls

NATO’s revised AI strategy elevates responsible-use principles, TEV&V, interoperability, and adversarial-risk monitoring as operational priorities. [40]

The UK MOD’s JSP 936 (2024) and follow-on RAISO implementation reporting (2025) show concrete institutionalization patterns: lifecycle governance, assurance, ethical-principle operationalization, and named senior accountability roles. [41][42]

The U.S.-led Political Declaration process (State Department) and UN General Assembly work on AI in the military domain reinforce lifecycle applicability of international law and responsibility norms. [43][44]

Implication:

- The governance baseline is shifting from principle-only to role/process/assurance structures.
- ACP should assume coalition interoperability requires policy/provenance/evidence exchange standards, not just API compatibility.

## B.5 Accountability problem is architectural, not rhetorical

SIPRI/ICRC analysis emphasizes a persistent point: accountability cannot be transferred to machines; legal/operational responsibility requires clearer human-machine role boundaries, traceability, and investigability of outcomes. [45][46]

Implication for ACP:

- Every high-consequence action path needs attributable decision provenance.
- Model/tool outputs are insufficient evidence by themselves.
- Evidence envelopes should include intent, scope, context hash, tool/action trace, and post-action state checks.

## B.6 Industrial scaling signal: autonomy is being procured as volume capability

DIU’s Replicator framing (Replicator-1 and Replicator-2) explicitly ties autonomy to delivery speed, volume, and iterative fielding in support of operational demand. [47]

Implication:

- Once autonomy shifts to volume procurement logic, governance debt compounds quickly.
- ACP needs to be in the acquisition gate, not added post-fielding.

## B.7 Warfighting postulates for ACP

The following postulates now look supportable from the combined evidence set:

1. **Tempo postulate:** Software-mediated delegation can outpace human-only coordination loops in contested environments.
2. **Fragility postulate:** Without control-plane governance, autonomy amplifies failure/compromise propagation.
3. **Accountability postulate:** Legal/command responsibility at machine speed requires runtime provenance and auditable constraints.
4. **Interoperability postulate:** Protocol-level portability without protocol-level governance is an adversary advantage.
5. **Resilience postulate:** Durable advantage depends on degraded-mode operation and rapid reconstitution, not perfect uptime.

## B.8 ACP minimum warfighting requirement set (v0)

### Authority and scope

- Typed trust scopes for agents, tools, data domains, and effects.
- Commander-approved delegation manifests with expiry and revocation.

### Policy and enforcement

- Inline policy decision points for tool calls, cross-agent messaging, and external actions.
- Consequence-tiered controls (observe-only, recommend, execute-with-checkpoint, execute-without-checkpoint).

### Evidence and auditability

- Default capture of action trajectory and evidence receipts.
- Tamper-evident logs sufficient for after-action legal and operational review.

### Degraded-mode behavior

- Explicit EW/comms-loss policies (autonomy downgrade, mission abort, local fallback constraints).
- Deterministic rejoin and resync behaviors.

### Supply-chain and skill safety

- Signed skills/connectors, provenance attestations, revocation channels.
- Runtime sandboxing and scoped credential brokerage.

### Evaluation and release

- Mission-context eval gates, adversarial injection suites, drift alarms.
- No-scale without passing eval + safety case.

## B.9 Immediate expansion backlog (next research pass)

1. Build comparative matrix: NATO/UK/U.S./UN governance requirements mapped to ACP control primitives.
2. Add campaign-level case studies (Ukraine, Red Sea, ISR-to-fire integration) with common failure modes.
3. Quantify a proposed **Delegation-to-Effect (D2E)** metric family for ACP performance tracking.
4. Draft ACP red-team scenarios for contested data, deceptive tools, and supply-chain compromise.
5. Add acquisition language templates to force ACP conformance in contracts and source selections.

## Additional references for ACP warfighting imperative

35. **GAO** — Defense Command and Control: Further Progress Hinges on Establishing a Comprehensive Framework (Apr 2025)  
    <https://files.gao.gov/reports/GAO-25-106454/index.html>
36. **CSIS** — Ukraine’s Future Vision and Current Capabilities for Waging AI-Enabled Autonomous Warfare (Mar 2025)  
    <https://www.csis.org/analysis/ukraines-future-vision-and-current-capabilities-waging-ai-enabled-autonomous-warfare>
37. **CSIS** — How Russia Is Reshaping Command and Control for AI-Enabled Warfare (Feb 2026)  
    <https://www.csis.org/analysis/how-russia-reshaping-command-and-control-ai-enabled-warfare>
38. **RAND** — How Could Artificial Intelligence Shape the Future of War? (2026)  
    <https://www.rand.org/pubs/research_reports/RRA4316-1.html>
39. **RAND** — Strategic competition in the age of AI: Emerging risks and opportunities from military use of AI (2024)  
    <https://www.rand.org/pubs/research_reports/RRA3295-1.html>
40. **NATO** — Summary of NATO’s revised AI strategy (Jul 2024)  
    <https://www.nato.int/en/about-us/official-texts-and-resources/official-texts/2024/07/10/summary-of-natos-revised-artificial-intelligence-ai-strategy>
41. **UK MOD (GOV.UK)** — JSP 936: Dependable Artificial Intelligence in defence (Part 1 directive) (Nov 2024)  
    <https://www.gov.uk/government/publications/jsp-936-dependable-artificial-intelligence-ai-in-defence-part-1-directive>
42. **UK MOD (GOV.UK)** — Laying the Groundwork: Responsible AI Senior Officers’ Report 2025 (Oct 2025)  
    <https://www.gov.uk/government/publications/laying-the-groundwork-responsible-ai-senior-officers-report-2025>
43. **U.S. Department of State** — Political Declaration on Responsible Military Use of Artificial Intelligence and Autonomy (updated 2024 context)  
    <https://www.state.gov/bureau-of-arms-control-deterrence-and-stability/political-declaration-on-responsible-military-use-of-artificial-intelligence-and-autonomy>
44. **UNODA** — Artificial intelligence in the military domain (including UNGA resolution 79/239 context)  
    <https://disarmament.unoda.org/en/our-work/emerging-challenges/artificial-intelligence-military-domain>
45. **SIPRI** — Retaining Human Responsibility in the Development and Use of Autonomous Weapon Systems (Oct 2022)  
    <https://www.sipri.org/publications/2022/policy-reports/retaining-human-responsibility-development-and-use-autonomous-weapon-systems-accountability>
46. **ICRC Law & Policy Blog** — Three lessons on AWS regulation to ensure accountability for IHL violations (Mar 2023)  
    <https://blogs.icrc.org/law-and-policy/2023/03/02/three-lessons-autonomous-weapons-systems-ihl/>
47. **DIU** — The Replicator Initiative (updated 2025)  
    <https://www.diu.mil/replicator>
48. **Arms Control Association** — AI and Nuclear Command and Control: It’s Even More Complicated Than You Think (Sep 2025)  
    <https://www.armscontrol.org/act/2025-09/features/artificial-intelligence-and-nuclear-command-and-control-its-even-more>

## Build target for review

- Generated `.tex` source path (internal): `Whitepaper/writing/notes/tex/2026-02-12-annex-a-supporting-notes-v2.tex`
- Generated PDF artifact path (internal): `out/memos/2026-02-12-annex-a-supporting-notes-v2.pdf`
- Publication status: **draft / non-published**.
