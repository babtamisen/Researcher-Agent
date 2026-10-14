# v0.2 candidate verification report

Status: prepared for Gateway-based retesting, not runtime-accepted.

## Changes verified locally
- Essential accuracy, citation and final-presentation rules added to SOUL.md.
- AGENTS.md requires explicit verification reads even on short numerical tasks.
- Verification reference forbids unsupported overlapping-window totals and requires a liquidity-basis reconciliation.
- The worked revised-series answer was removed from runtime references.
- Original sixteen fixtures retained as regression cases, not fresh blind tests.
- Runtime instructions contain no labeled benchmark cases or worked benchmark answers. A broad substring scan initially flagged ordinary words such as conflict and no-change; targeted contamination checks distinguish those terms from case labels.
- Relative Markdown links and JSON structure checked, and Git patch whitespace checked.
- Archive integrity and tracked-file byte comparison checked during packaging.

SOUL.md is within the reported generic per-file budget, but that is not proof of candidate injection. Actual injection/truncation must be observed through the normal Gateway/Codex session.

## Pending
Actual model acceptance, instruction loading, reference reads, tool parity, research accuracy, no-delivery controls, and validated interruption-recovery supervision remain pending. No live configuration or GitHub repository was changed here.

These instruction requirements are not an automated validator. An actual runtime evaluation must show whether the tested model follows them reliably. Preserve the original workspace until a separate activation decision.

Final review was performed by the author. Use the retest handoff for the administrator/evaluator procedure.
