# ACP-RA diagrams

Drop diagram assets used by the paper here.

## Files
- `acp_ov1_simplified.dot` (source) → `acp_ov1_simplified.png` + `acp_ov1_simplified.svg`
  - Caption: **Agent Control Plane (ACP) OV-1 (Color-Coded, Outline-First)**
  - Usage: referenced in the paper as the conceptual view with outline-first color coding for existing baseline, ACP-RA-specific control-plane components, and runtime integration.

- `acp_action_flow.dot` (source) → `acp_action_flow.png` + `acp_action_flow.svg`
  - Caption: **Policy-Enforced Tool Invocation (Action Envelope)**
  - Usage: referenced in the paper as the action loop: intent → policy → mediated action → evidence.

- `acp_governance_lifecycle_compact.dot` (source) → `acp_governance_lifecycle_compact.png` + `acp_governance_lifecycle_compact.svg`
  - Caption: **Governance-as-Code Lifecycle (Compact)**
  - Usage: referenced in the paper as the governance loop: artifacts → CI → evals → approval → promote → enforce → evidence → cATO.
