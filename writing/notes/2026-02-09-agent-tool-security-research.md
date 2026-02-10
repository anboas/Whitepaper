---
title: "Notes: Research that shaped ACP-RA (agent security + tool use)"
date: 2026-02-09
summary: "Reading notes on prompt injection, tool-use training, and execution-based evaluation that drove key ACP-RA design choices (gateways, envelopes, evidence, and anti-replay)."
status: published
type: note
tags:
  - acp-ra
  - agents
  - security
  - tool-use
  - prompt-injection
  - evaluation
---

These notes capture the research thread that informed **ACP-RA** before publication (paper date: 2026-02-10). The theme across everything I read is simple: once an agent can call tools, the system’s real risks and real failures are almost never “bad text”; they’re **authority leakage**, **untrusted data becoming control**, and **execution mistakes** at the tool boundary.

## Papers I read closely (and why they mattered)

### Quick index

| # | Paper | Link | Core problem | ACP-RA takeaway |
|---:|---|---|---|---|
| 1 | Prompt injection design patterns | [arXiv](https://arxiv.org/abs/2506.08837) | Untrusted inputs hijack tool-using agents | Separate planes; mediate side effects; treat data plane as untrusted |
| 2 | Prompt injections → protocol exploits | [arXiv](https://arxiv.org/abs/2506.23260) | Attacks escalate from strings to workflows | Design for adversarial workflows; stop confused-deputy chains |
| 3 | Toolformer | [arXiv](https://arxiv.org/abs/2302.04761) | Tool use needs explicit training signals | Schemas + receipts + execution-based eval |
| 4 | ToolLLM | [arXiv](https://arxiv.org/abs/2307.16789) | Tool catalogs get huge; correctness is brittle | Tool plane needs discovery/ranking, validation, retries, observability |
| 5 | ReAct | [arXiv](https://arxiv.org/abs/2210.03629) | Agents drift without grounded action/observation loops | Mediate actions; treat observations as untrusted data |
| 6 | MRKL Systems | [arXiv](https://arxiv.org/abs/2205.00445) | Monolithic models are the wrong abstraction for capability | Broker capability through registries/scopes and gateways |
| 7 | SWE-bench | [arXiv](https://arxiv.org/abs/2310.06770) | “Looks right” ≠ works; eval must be end-to-end | Gate upgrades on execution-based regression suites |

Expanded notes per paper below.

### 1) Design Patterns for Securing LLM Agents against Prompt Injections
Link: https://arxiv.org/abs/2506.08837

- **Core problem:** Tool-using agents ingest untrusted text (web pages, emails, tickets) that can smuggle instructions and hijack behavior.
- **Big idea:** Treat prompt injection as a *systems security problem*: enforce trust boundaries, constrain capabilities, and build defense-in-depth rather than “better prompting.”
- **ACP-RA lesson:** The only stable fix is architectural: separate planes, mediate side effects, and treat the data plane as explicitly untrusted.

### 2) From Prompt Injections to Protocol Exploits: Threats in LLM-Powered AI Agents Workflows
Link: https://arxiv.org/abs/2506.23260

- **Core problem:** Once agents participate in workflows, attackers can escalate from text injection into **protocol-level exploits** (tool misuse, chain-of-calls, confused deputy).
- **Big idea:** The attack surface expands from “prompt” to the full workflow graph: tool schemas, connectors, retries, permissions, and state.
- **ACP-RA lesson:** Design around **adversarial workflows**, not just adversarial strings.

### 3) Toolformer: Language Models Can Teach Themselves to Use Tools
Link: https://arxiv.org/abs/2302.04761

- **Core problem:** Models don’t reliably learn correct tool invocation from next-token training alone.
- **Big idea:** Generate tool-use supervision at scale by letting the model propose tool calls, execute them, and train on outcomes.
- **ACP-RA lesson:** Tool use is a distinct competency: it wants **schemas**, **execution receipts**, and **evaluation** tied to real calls.

### 4) ToolLLM: Facilitating Large Language Models to Master Thousands of Real-World APIs
Link: https://arxiv.org/abs/2307.16789

- **Core problem:** Real tool ecosystems are huge; correctness depends on endpoint selection and argument fidelity, not eloquence.
- **Big idea:** Scale training and evaluation around large API catalogs, emphasizing execution-valid tool use.
- **ACP-RA lesson:** At scale, the tool plane becomes a product: **discovery/ranking**, **schema validation**, **retries**, and **observability** become first-class requirements.

### 5) ReAct: Synergizing Reasoning and Acting in Language Models
Link: https://arxiv.org/abs/2210.03629

- **Core problem:** Pure “reasoning-only” prompting drifts, and pure “act-now” tool use is brittle; agents need a disciplined loop.
- **Big idea:** Interleave reasoning with actions and observations so the model stays grounded and can correct itself.
- **ACP-RA lesson:** The *agent loop* is an interface: actions should be mediated (gateways), and observations should be treated as untrusted inputs unless proven otherwise.

### 6) MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning
Link: https://arxiv.org/abs/2205.00445

- **Core problem:** One monolithic model is a poor place to concentrate every capability (math, search, databases, policy, etc.).
- **Big idea:** Route to specialized tools/experts; keep the LLM as coordinator rather than the executor of everything.
- **ACP-RA lesson:** This reinforces the control-plane thesis: capability should be **explicitly brokered** through registries/scopes and mediated gateways, not implicitly granted by “smartness.”

### 7) SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
Link: https://arxiv.org/abs/2310.06770

- **Core problem:** “Looks right” is not “works”; evaluation must reflect real-world tasks with real constraints.
- **Big idea:** Test agents on end-to-end issue resolution where correctness is measurable.
- **ACP-RA lesson:** Governance needs an evaluation harness. Model/tool upgrades should be gated on **execution-based regression suites**, not vibes.

## How this fed directly into ACP-RA

These papers are why ACP-RA treats tool use as governed infrastructure, not “an agent trick.” Concretely, they pushed me toward:

- **Distinct gateways by plane**: tool/action, context/data, model, and inter-agent; each with its own policy surface and audit story.
- **Typed envelopes** instead of “prompt blobs” as transport for anything that causes side effects or crosses trust boundaries.
- **Evidence-by-default**: every attempted side effect should emit a structured record (request + result), sufficient for replay and continuous authorization.
- **Anti-replay and integrity** for agent-to-agent comms: once swarms exist, messaging is an adversarial channel unless proven otherwise.

In short: *mediation* is the architecture. The model can suggest; only gateways can do.

## Lessons I did NOT integrate into ACP-RA (yet)

This is the explicit backlog of research-derived lessons I still want folded into the paper (or companion material):

1) **Prompt-injection countermeasures as a named pattern set**
   - ACP-RA discusses trust boundaries, but it should include a compact “prompt injection defense” inventory (instruction/data separation, taint/provenance, allowlisted tool intents, and safe rendering of untrusted content).

2) **Execution-based evaluation as a first-class governance artifact**
   - ACP-RA references evaluation, but it should define a minimal ToolBench/SWE-bench-like stance: task suites, pass/fail criteria tied to real execution, and regression gates tied to model/tool upgrades.

3) **Tool discovery and disambiguation at scale**
   - ToolLLM makes clear that large catalogs require ranking and disambiguation controls. ACP-RA should be more explicit about how the tool registry, retrieval layer, and policy interact (including “deny by default unless the work unit explicitly needs it”).

4) **Explicit connector threat model**
   - Workflow attacks aren’t only about tools, but about connectors (email, tickets, browser automation, RPA). ACP-RA should add a “connector onboarding” checklist: attestation, scopes, safe defaults, logging, and kill-switches.

5) **Open science / artifact stance for credibility**
   - Even as a whitepaper, ACP-RA should list what artifacts exist (schemas, example envelopes, test harnesses) and what can’t be shared (and why). This increases trust and makes the architecture operationally actionable.

## The meta-lesson (the reason ACP-RA looks the way it does)

All of these papers converge on a single conclusion: **the agent is not the unit of trust**. The unit of trust is the *governed interface* between untrusted inputs, model outputs, and real-world side effects. That’s why ACP-RA is a control plane and not “prompt engineering guidance.”
