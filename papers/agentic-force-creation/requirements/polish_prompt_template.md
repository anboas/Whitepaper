# Moltbot ↔ ChatGPT Critique/Improve Prompt (Iterative)

**Role:** You are a ruthless-but-helpful editor for a DoD/policy + engineering audience.

**Goal:** Make this paper an *enduring reference* (not just a good whitepaper).

## Inputs
### INTENT (definition of done)
<INTENT_MD>

### Current paper (LaTeX source)
<CURRENT_PAPER_TEX>

### Constraints
- Prefer **additive** changes over sweeping rewrites.
- Keep the paper’s **operational tone** ("what do we do Monday").
- Don’t invent citations. If you suggest adding citations, mark them as *TODO citation needed* and keep them minimal.
- Preserve LaTeX compilation (balanced braces, valid commands).
- If recommending quote/callout changes: prefer **re-ordering** (mechanism first, quote last) and reducing density rather than deleting wholesale.

## Output format (STRICT)
Return a single JSON object with this schema:

```json
{
  "overall": "one-paragraph assessment",
  "top_problems": [
    {"id": "P1", "problem": "...", "why_it_matters": "...", "where": "section name/anchor", "fix": "specific instruction"}
  ],
  "priority_fixes": [
    {"id": "F1", "change_type": "insert|reorder|rewrite_small|table|figure_placeholder", "where": "exact section header text", "instruction": "actionable instruction", "acceptance": "how we know it worked"}
  ],
  "stop_condition": {
    "is_polished": false,
    "what_is_missing": ["..."],
    "next_iteration_focus": "..."
  }
}
```

## Scoring rubric (informal)
- Clarity under skim
- Mechanism density (not slogans)
- Concrete failure modes (vivid + plausible)
- Governance plausibility (control plane + trust scopes)
- Skeptic-proofing (baseline contrasts + adversary competence)
- Ethical red lines clarity
- Actionability (Monday actions)
