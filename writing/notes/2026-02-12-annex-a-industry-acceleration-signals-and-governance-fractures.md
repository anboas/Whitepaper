---
title: "Research Paper (Draft): ACP Mission Control, Agent Orchestration, and Swarm Warfare"
date: 2026-02-12
summary: "Structured research paper connecting multi-agent orchestration, swarm operations, C2 modernization, and governance constraints to ACP-RA design and Delegated Autonomy Directorate (DAD) decisions."
status: draft
type: note
tags:
  - acp-ra
  - dad
  - mission-control
  - swarms
  - orchestration
  - governance
  - research
---

## Abstract

This paper argues that Agent Control Plane (ACP) capability is a warfighting imperative because the decisive variable is no longer model quality alone, but governed delegation throughput under contested conditions. Across military and commercial ecosystems, agent operations are converging on the same structural need: Mission Control for autonomous execution.

The evidence shows six compounding realities:

1. multi-agent orchestration is becoming the default scaling pattern,
2. swarms and low-cost autonomy compress operational timelines,
3. C2 integration debt remains a binding constraint,
4. governance/accountability obligations are hardening,
5. adversarial pressure concentrates at protocol, context, and connector boundaries,
6. acquisition pathways are already scaling autonomy faster than traditional governance mechanisms.

Conclusion: ACP is not a feature layer. It is command infrastructure for delegated autonomy.

## 1) Research objective and decision linkage

### Primary research objective

Build a coherent, evidence-grounded model of how agent orchestration and swarms change modern conflict, and translate that into:

- ACP-RA design primitives,
- DAD organizational authorities,
- near-term implementation priorities.

### Decision linkage

- **ACP-RA feed:** what must be engineered and enforced in the control plane.
- **DAD memo feed:** what must be institutionally governed, mandated, and audited.

## 2) Method and analytical framework

### 2.1 Evidence corpus

This paper integrates three evidence layers:

1. **Public operational/strategic evidence** (labs, policy, defense reporting, think tanks, standards signals).
2. **Academic evidence** (multi-agent systems, MARL, swarms, orchestration, safety/governance, adversarial resilience).
3. **Programmatic implementation evidence** (CJADC2 constraints, Replicator timelines, C-UAS scaling, protocol governance shifts).

### 2.2 Analytical structure

To preserve coherence across a broad source base, the paper applies a claim-evidence-implication structure in each section:

- **Claim:** what strategic or operational condition is changing.
- **Evidence:** policy, operational, and academic signals that establish the change.
- **Implication:** what ACP-RA and DAD must do differently in architecture and governance.

The paper is organized by mission-relevant topic clusters rather than chronology so each section can be read as a standalone decision input.

## 3) Topic cluster A: Mission Control and C2 compression

### Core claim A1

Warfighting advantage increasingly depends on reducing delegation-to-effect latency while preserving bounded control.

### Key evidence threads

- GAO CJADC2 reporting: progress exists, but framework, measurement, and integration barriers remain substantial. [35]
- Frontier-style enterprise agent platforms frame deployment/governance stack as the bottleneck, not model IQ alone. [1]
- Multi-agent platform announcements now emphasize orchestration, role delegation, and operational boundaries. [49][50][51]

### Implication for ACP-RA

ACP must implement Mission Control functions as core control-plane behaviors:

- intent packets,
- delegation scopes,
- policy checkpoints,
- effect verification,
- exception and rollback pathways.

## 4) Topic cluster B: Swarms, volume autonomy, and force survivability

### Core claim B1

Scale changes everything: command quality degrades unless orchestration and policy enforcement are built for saturation conditions.

### Key evidence threads

- CNAS: cheap drone mass creates persistent threat; layered C-UAS and scaled defenses are necessary. [54]
- CNA: PRC swarm research is explicitly connected to Taiwan-relevant scenarios and lessons from ongoing conflicts. [55]
- Army sustainment evidence shows swarm concepts moving into logistics and support-area security, not only maneuver units. [53]
- Replicator 1/2 confirms autonomy and counter-autonomy are moving through accelerated fielding paths. [47][56]

### Implication for ACP-RA

ACP cannot assume sparse event flow. It must be saturation-resilient:

- queue-aware prioritization,
- consequence-tier gating,
- budget-aware action authorization,
- deterministic degraded-mode operation.

## 5) Topic cluster C: Interoperability, protocols, and orchestration ecosystems

### Core claim C1

Interoperability standards increase both coordination power and attack surface. Protocol governance becomes decisive.

### Key evidence threads

- A2A and MCP trajectory indicates rapid protocolization of agent-to-agent and tool-context interactions. [5][6][51][52]
- Linux Foundation governance move for A2A suggests ecosystem-wide standardization momentum. [52]
- Multi-vendor enterprise platform competition is converging on orchestration + identity + operational controls. [49][50][51]

### Implication for ACP-RA

ACP should enforce protocol-bound trust, not app-bound trust:

- signed capability cards,
- attested agent identity,
- constrained delegation chains,
- anti-replay and provenance at message boundaries.

## 6) Topic cluster D: Safety, legal accountability, and command responsibility

### Core claim D1

At machine speed, accountability is impossible without architectural provenance.

### Key evidence threads

- Responsible-use policy frameworks are becoming lifecycle-oriented, not principle-only. [40][41][42][43][44]
- ICRC/SIPRI logic remains central: responsibility is retained by humans and institutions; it cannot transfer to systems. [45][46]
- Frontier risk artifacts emphasize deceptive/failed tool-use conditions as practical risk domains. [12][13][14]

### Implication for ACP-RA

Every high-consequence action path requires attributable evidence:

- who delegated,
- what scope was active,
- what policy checks fired,
- what tools executed,
- what verified effect occurred.

## 7) Topic cluster E: Adversarial resilience and contested operation

### Core claim E1

The highest-value attack surfaces are no longer only endpoints; they are orchestration pathways and context channels.

### Key evidence threads

- OpenClaw/ClawHub incidents and follow-on warnings demonstrate agent supply-chain attack behavior in the wild. [25][26][27][28]
- RAND and CSIS analyses stress adaptive adversaries, contested information advantage, and distributed mission command logic. [38][39]
- Adversarial MARL and deception-attack literature supports architecture-level robustness requirements.

### Implication for ACP-RA

ACP should treat resilience as a control objective with explicit design controls:

- partition-safe execution,
- context provenance and confidence fusion,
- connector attestation,
- rapid revocation/reconstitution.

## 8) Topic cluster F: Infrastructure, energy, and industrial base constraints

### Core claim F1

Compute and power constraints shape autonomy feasibility and tempo as much as algorithmic capability.

### Key evidence threads

- Capital and power are increasingly first-order autonomy enablers/constraints. [29][30][31][32]
- Operational concentration risk rises when autonomy depends on fragile infrastructure concentration.

### Implication for ACP-RA

ACP must support heterogeneous model tiers and edge fallback profiles, including low-connectivity and low-power execution envelopes.

## 9) Synthesis: ACP-RA design primitives

The following primitives emerge as non-optional from cross-topic synthesis.

### 9.1 Authority primitives

- Commander Intent Packet (CIP)
- Delegation Authority Token (DAT)
- Trust Scope Manifest (TSM)

### 9.2 Enforcement primitives

- action-time policy checks
- consequence-tiered authorization
- cross-agent interaction control

### 9.3 Evidence primitives

- action trajectory logging
- evidence envelopes (context hash + tool receipts + effect verification)
- forensic replay support

### 9.4 Resilience primitives

- degraded-mode profiles
- partition-safe operation
- rejoin and reconstitution controls

### 9.5 Supply-chain primitives

- signed skills/connectors
- provenance attestation
- emergency revocation channels

### 9.6 Evaluation primitives

- mission-context benchmark suites
- adversarial injection suites
- drift-triggered rollback rules

## 10) Direct feed into DAD memo (organizational design)

### 10.1 Why DAD remains structurally necessary

No single functional lane can own delegated autonomy at force scale. DAD is required as a cross-domain control authority integrating doctrine, policy, and technical enforcement.

### 10.2 Minimum DAD authorities (research-derived)

- approve/deny delegation scope baselines,
- enforce no-conformance/no-scale rule,
- mandate evidence and telemetry standards,
- direct degraded-mode posture policy,
- suspend tool registries or inter-agent channels,
- run autonomy red-team and containment drills,
- require pre-scale eval-pack conformance.

### 10.3 Initial implementation sequence

- **Phase 1:** authority and baseline publication,
- **Phase 2:** enforcement plumbing + controlled fieldings,
- **Phase 3:** compulsory conformance and scored oversight.

## 11) Conclusions

1. Multi-agent orchestration and swarm operations are not hypothetical future capabilities; they are current operational realities.
2. C2 and mission-control quality now bound autonomy effectiveness more than isolated model quality.
3. Protocol and connector surfaces are becoming primary trust boundaries.
4. Governance without operational enforcement is inadequate under machine-speed delegation.
5. ACP-RA should be treated as warfighting infrastructure, and DAD as its institutional control authority.

## 12) Policy/operational source references

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
43. **U.S. Department of State** — Political Declaration on Responsible Military Use of Artificial Intelligence and Autonomy  
    <https://www.state.gov/bureau-of-arms-control-deterrence-and-stability/political-declaration-on-responsible-military-use-of-artificial-intelligence-and-autonomy>
44. **UNODA** — Artificial intelligence in the military domain (incl. UNGA 79/239 context)  
    <https://disarmament.unoda.org/en/our-work/emerging-challenges/artificial-intelligence-military-domain>
45. **SIPRI** — Retaining Human Responsibility in the Development and Use of Autonomous Weapon Systems (Oct 2022)  
    <https://www.sipri.org/publications/2022/policy-reports/retaining-human-responsibility-development-and-use-autonomous-weapon-systems-accountability>
46. **ICRC Law & Policy Blog** — Three lessons on AWS regulation to ensure accountability for IHL violations (Mar 2023)  
    <https://blogs.icrc.org/law-and-policy/2023/03/02/three-lessons-autonomous-weapons-systems-ihl/>
47. **DIU** — The Replicator Initiative (updated 2025)  
    <https://www.diu.mil/replicator>
48. **Arms Control Association** — AI and Nuclear Command and Control: It’s Even More Complicated Than You Think (Sep 2025)  
    <https://www.armscontrol.org/act/2025-09/features/artificial-intelligence-and-nuclear-command-and-control-its-even-more>
49. **Microsoft Copilot Blog** — Multi-agent orchestration announcements at Build 2025  
    <https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/multi-agent-orchestration-maker-controls-and-more-microsoft-copilot-studio-announcements-at-microsoft-build-2025/>
50. **Google Cloud Blog** — Build and manage multi-system agents with Vertex AI (Apr 2025)  
    <https://cloud.google.com/blog/products/ai-machine-learning/build-and-manage-multi-system-agents-with-vertex-ai>
51. **Google Cloud Blog** — Agent2Agent protocol (A2A) is getting an upgrade (Jul 2025)  
    <https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade>
52. **Google Developers Blog** — Google Cloud donates A2A to Linux Foundation (Jun 2025)  
    <https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/>
53. **U.S. Army** — Swarm Technology in Sustainment Operations (Jan 2025)  
    <https://www.army.mil/article/282467/swarm_technology_in_sustainment_operations>
54. **CNAS** — Countering the Swarm: Protecting the Joint Force in the Drone Age (Sep 2025)  
    <https://s3.us-east-1.amazonaws.com/files.cnas.org/documents/Report_CUAS_Defense_Sep-2025_final.pdf>
55. **CNA** — PRC Concepts for UAV Swarms in Future Warfare (Oct 2025)  
    <https://www.cna.org/analyses/2025/10/prc-concepts-for-uav-swarms-in-future-warfare>
56. **U.S. Secretary of Defense Memorandum** — Replicator 2 Direction and Execution (Sep 27, 2024)  
    <https://s3.us-gov-west-1.amazonaws.com/assets.diu.mil/3nanhbfkr0pc/1dkJGhMeAgPldz1nnIwabK/abf85531a4281cddab6b0d8c953440e2/REPLICATOR-2-MEMO-SD-SIGNED__1_.pdf>

## 13) Academic source library (topic-grouped)

### MARL core
1. Multi-Agent Reinforcement Learning: Independent vs. Cooperative Agents (1993), cited by 1789. <https://doi.org/10.1016/b978-1-55860-307-3.50049-6>
2. Counterfactual Multi-Agent Policy Gradients (2018), cited by 1543. <https://doi.org/10.1609/aaai.v32i1.11794>
3. Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (2017), cited by 1014. <http://arxiv.org/abs/1706.02275>
4. Cooperative Multi-agent Control Using Deep Reinforcement Learning (2017), cited by 846. <https://doi.org/10.1007/978-3-319-71682-4_5>
5. Multi-agent deep reinforcement learning: a survey (2021), cited by 726. <https://doi.org/10.1007/s10462-021-09996-w>
6. QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning (2018), cited by 475. <http://arxiv.org/abs/1803.11485>
7. Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning (2020), cited by 429. <http://arxiv.org/abs/2003.08839>
8. A review of cooperative multi-agent deep reinforcement learning (2022), cited by 404. <https://doi.org/10.1007/s10489-022-04105-y>
9. Multi-Agent Reinforcement Learning: A Review of Challenges and Applications (2021), cited by 315. <https://doi.org/10.3390/app11114948>
10. Robust Multi-Agent Reinforcement Learning via Minimax Deep Deterministic Policy Gradient (2019), cited by 279. <https://doi.org/10.1609/aaai.v33i01.33014213>
11. QTRAN: Learning to Factorize with Transformation for Cooperative Multi-Agent Reinforcement Learning (2019), cited by 222. <https://doi.org/10.48550/arxiv.1905.05408>
12. Multi-Agent Deep Reinforcement Learning for Multi-Robot Applications: A Survey (2023), cited by 140. <https://doi.org/10.3390/s23073625>
13. Dealing with Non-Stationarity in Multi-Agent Deep Reinforcement Learning (2019), cited by 124. <http://arxiv.org/abs/1906.04737>
14. Value-Decomposition Networks For Cooperative Multi-Agent Learning (2017). <https://arxiv.org/abs/1706.05296>
15. Learning to Communicate with Deep Multi-Agent Reinforcement Learning (2016). <https://arxiv.org/abs/1605.06676>

### Swarm robotics + human-swarm interaction
1. Swarm robotics: a review from the swarm engineering perspective (2013), cited by 1638. <https://doi.org/10.1007/s11721-012-0075-2>
2. A Survey on Aerial Swarm Robotics (2018), cited by 604. <https://doi.org/10.1109/tro.2018.2857475>
3. Swarm of micro flying robots in the wild (2022), cited by 490. <https://doi.org/10.1126/scirobotics.abm5954>
4. A review of swarm robotics tasks (2015), cited by 428. <https://doi.org/10.1016/j.neucom.2015.05.116>
5. Swarm Robotic Behaviors and Current Applications (2020), cited by 413. <https://doi.org/10.3389/frobt.2020.00036>
6. Human Interaction With Robot Swarms: A Survey (2015), cited by 387. <https://doi.org/10.1109/thms.2015.2480801>
7. Swarm Robotics: Past, Present, and Future [Point of View] (2021), cited by 327. <https://doi.org/10.1109/jproc.2021.3072740>
8. Search and tracking algorithms for swarms of robots: A survey (2015), cited by 180. <https://doi.org/10.1016/j.robot.2015.08.010>
9. Predictive control of aerial swarms in cluttered environments (2021), cited by 151. <https://doi.org/10.1038/s42256-021-00341-y>
10. Human swarm interaction for radiation source search and localization (2008), cited by 112. <https://doi.org/10.1109/sis.2008.4668287>
11. Human Swarm Interaction: An Experimental Study of Two Types of Interaction with Foraging Swarms (2013), cited by 104. <https://doi.org/10.5898/jhri.2.2.kolling>
12. Mean-field models in swarm robotics: a survey (2019), cited by 94. <https://doi.org/10.1088/1748-3190/ab49a4>

### LLM agents + orchestration
1. A survey on large language model based autonomous agents (2024), cited by 797. <https://doi.org/10.1007/s11704-024-40231-1>
2. A survey on LLM-based multi-agent systems: workflow, infrastructure, and challenges (2024), cited by 153. <https://doi.org/10.1007/s44336-024-00009-2>
3. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (2023), cited by 138. <http://arxiv.org/abs/2308.08155>
4. ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate (2023), cited by 51. <http://arxiv.org/abs/2308.07201>
5. Large Language Model based Multi-Agents: A Survey of Progress and Challenges (2024), cited by 50. <http://arxiv.org/abs/2402.01680>
6. Exploring Large Language Model based Intelligent Agents: Definitions, Methods, and Prospects (2024), cited by 35. <http://arxiv.org/abs/2401.03428>
7. Personal LLM Agents: Insights and Survey about the Capability, Efficiency and Security (2024), cited by 30. <http://arxiv.org/abs/2401.05459>
8. Understanding the planning of LLM agents: A survey (2024), cited by 26. <http://arxiv.org/abs/2402.02716>
9. Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate (2023), cited by 26. <http://arxiv.org/abs/2305.19118>
10. LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision and the Road Ahead (2024), cited by 8. <http://arxiv.org/abs/2404.04834>
11. CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society (2023). <https://arxiv.org/abs/2303.17760>
12. AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors (2023). <https://arxiv.org/abs/2308.10848>
13. MetaGPT: Meta Programming for Multi-Agent Collaborative Framework (2023). <https://arxiv.org/abs/2308.00352>
14. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (2024). <https://arxiv.org/abs/2405.15793>

### Safety, governance, and legal accountability
1. A comprehensive survey on safe reinforcement learning (2015), cited by 1191. <https://jmlr.csail.mit.edu/papers/volume16/garcia15a/garcia15a.pdf>
2. Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning (2022), cited by 594. <https://doi.org/10.1146/annurev-control-042920-020211>
3. Trustworthy artificial intelligence (2020), cited by 507. <https://doi.org/10.1007/s12525-020-00441-4>
4. Meaningful Human Control over Autonomous Systems: A Philosophical Account (2018), cited by 405. <https://doi.org/10.3389/frobt.2018.00015>
5. On banning autonomous weapon systems: human rights, automation, and the dehumanization of lethal decision-making (2012), cited by 339. <https://doi.org/10.1017/s1816383112000768>
6. A Review of Trustworthy and Explainable Artificial Intelligence (XAI) (2023), cited by 225. <https://doi.org/10.1109/access.2023.3294569>
7. Autonomous weapons systems, killer robots and human dignity (2018), cited by 176. <https://doi.org/10.1007/s10676-018-9494-0>
8. Autonomous Weapons and International Humanitarian Law: Advantages, Open Technical Questions and Legal Issues to be Clarified (2014), cited by 113. <https://archive-ouverte.unige.ch/unige:37976>
9. Autonomous Weapon Systems and International Humanitarian Law: A Reply to the Critics (2012), cited by 101. <https://doi.org/10.2139/ssrn.2184826>
10. Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback (2023), cited by 88. <http://arxiv.org/abs/2307.15217>

### Adversarial robustness and resilience
1. Secure impulsive synchronization control of multi-agent systems under deception attacks (2018), cited by 324. <https://doi.org/10.1016/j.ins.2018.04.020>
2. Secure impulsive synchronization in Lipschitz-type multi-agent systems subject to deception attacks (2020), cited by 165. <https://doi.org/10.1109/jas.2020.1003297>
3. A study on cyber-security of autonomous and unmanned vehicles (2015), cited by 136. <https://doi.org/10.1177/1548512915575803>
4. Cooperative adaptive fault-tolerant control for multi-agent systems with deception attacks (2020), cited by 111. <https://doi.org/10.1016/j.jfranklin.2019.12.032>
5. Detection of Cyber-attacks to indoor real time localization systems for autonomous robots (2017), cited by 87. <https://doi.org/10.1016/j.robot.2017.10.006>
6. Fault-Tolerant secure consensus tracking of delayed nonlinear multi-agent systems with deception attacks and uncertain parameters via impulsive control (2019), cited by 85. <https://doi.org/10.1016/j.cnsns.2019.105043>
7. Enhancing Autonomous System Security and Resilience With Generative AI: A Comprehensive Survey (2024), cited by 60. <https://doi.org/10.1109/access.2024.3439363>
8. Failure-Scenario Maker for Rule-Based Agent using Multi-agent Adversarial Reinforcement Learning and its Application to Autonomous Driving (2019), cited by 57. <https://doi.org/10.24963/ijcai.2019/832>
9. Multi-Agent Adversarial Inverse Reinforcement Learning (2019), cited by 45. <http://arxiv.org/abs/1907.13220>
10. On the Robustness of Cooperative Multi-Agent Reinforcement Learning (2020). <https://arxiv.org/abs/2006.07538>

