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

These notes capture the research thread that informed **ACP-RA** before publication (paper date: 2026-02-10). The theme across everything we read is simple: once an agent can call tools, the system’s real risks and real failures are almost never “bad text”\; they’re **authority leakage**, **untrusted data becoming control**, and **execution mistakes** at the tool boundary.

## Papers we read closely (and why they mattered)

### 1) Design Patterns for Securing LLM Agents against Prompt Injections
Link: https://arxiv.org/abs/2506.08837

- **Core problem:** Tool-using agents ingest untrusted text (web pages, emails, tickets) that can smuggle instructions and hijack behavior.
- **Big idea:** Treat prompt injection as a *systems security problem*\: enforce trust boundaries, constrain capabilities, and build defense-in-depth rather than “better prompting.”
- **ACP-RA lesson:** The only stable fix is architectural: separate planes, mediate side effects, and make the data plane explicitly untrusted.

### 2) From Prompt Injections to Protocol Exploits: Threats in LLM-Powered AI Agents Workflows
Link: https://arxiv.org/abs/2506.23260

- **Core problem:** Once agents participate in workflows, attackers can escalate from text injection into **protocol-level exploits** (tool misuse, chain-of-calls, confused deputy).
- **Big idea:** The attack surface expands from “prompt” to the whole workflow graph: tool schemas, connectors, retries, permissions, and state.
- **ACP-RA lesson:** We must design around **adversarial workflows**, not just adversarial strings.

### 3) Toolformer: Language Models Can Teach Themselves to Use Tools
Link: https://arxiv.org/abs/2302.04761

- **Core problem:** Models don’t naturally learn reliable tool invocation from next-token training alone.
- **Big idea:** Generate tool-use supervision at scale by letting the model propose tool calls, execute them, and train on outcomes.
- **ACP-RA lesson:** Tool use is a distinct competency that benefits from explicit **tool schemas**, **execution receipts**, and **evaluation** that reflects real calls.

### 4) ToolLLM: Facilitating Large Language Models to Master Thousands of Real-World APIs
Link: https://arxiv.org/abs/2307.16789

- **Core problem:** Real tool ecosystems are huge; correctness depends on endpoint selection and argument fidelity, not eloquence.
- **Big idea:** Scale training and evaluation around large API catalogs, emphasizing execution-valid tool use.
- **ACP-RA lesson:** At scale, the tool plane becomes a product: **discovery/ranking**, **schema validation**, **retries**, and **observability** become first-class requirements.

## How this fed directly into ACP-RA

These papers are why ACP-RA treats tool use as governed infrastructure, not “an agent trick.” Concretely, they pushed us toward:

- **Distinct gateways by plane**: tool/action, context/data, model, and inter-agent\; each with its own policy surface and audit story.
- **Typed envelopes** instead of “prompt blobs” as transport for anything that causes side effects or crosses trust boundaries.
- **Evidence-by-default**: every attempted side effect should emit a structured record (request + result), sufficient for replay and continuous authorization.
- **Anti-replay and integrity** for agent-to-agent comms: once swarms exist, messaging is an adversarial channel unless proven otherwise.

In short: *mediation* is the architecture. The model can suggest; only gateways can do.

## Lessons we did NOT integrate into ACP-RA (yet)

This is the explicit backlog of research-derived lessons we should still fold into the paper (or companion material):

1) **Prompt-injection countermeasures as a named pattern set**
   - We talk about trust boundaries, but we should add a compact, explicit “prompt injection defense” pattern inventory (input sanitization, instruction/data separation, allowlisted tool intents, content provenance/taint).

2) **Execution-based evaluation as a first-class governance artifact**
   - We reference evaluation, but we should define a minimal “ToolBench-like” evaluation harness requirement: task suites, pass/fail criteria tied to real tool execution, and regression gates tied to model/tool upgrades.

3) **Tool discovery and disambiguation at scale**
   - ToolLLM makes clear that large catalogs require ranking and disambiguation controls. We should specify how the tool registry, retrieval layer, and policy interact (including “deny by default unless the task explicitly needs it”).

4) **Explicit connector threat model**
   - The workflow attacks aren’t only about tools, but about connectors (email, tickets, browser automation, RPA). We should add a “connector onboarding” checklist: attestation, scopes, safe defaults, logging, and kill-switches.

5) **Open science / artifact stance for credibility**
   - Even as a whitepaper, we should list what artifacts exist (schemas, example envelopes, test harnesses) and what we can’t share (and why). This increases trust and makes ACP-RA operationally actionable.

## The meta-lesson (the reason ACP-RA looks the way it does)

All of these papers converge on a single conclusion: **the agent is not the unit of trust**. The unit of trust is the *governed interface* between untrusted inputs, model outputs, and real-world side effects. That’s why ACP-RA is a control plane and not “prompt engineering guidance.”
