# Researcher 0.4 — supervised candidate

Start with OPENCLAW-INSTRUCTIONS.txt and ACCEPTANCE.md. This package is a test candidate, not production-approved.

Researcher retrieves and extracts original source rows; administrator checks definitions and executes unchanged deterministic tools; researcher drafts from an explicit review handoff; administrator reviews and renders. Model does not normalize the supplied liquidity claim into base USD. The adapter does that conversion from source value and scale. Calculator/adapter/renderer do NOT verify semantic source truth or enforce delivery.

No automatic runner, Gateway plugin, runtime approval gate or unattended cron integration is included. Administrator remains in the loop. This trade-off must not be concealed as an autonomous researcher upgrade. Existing job behavior remains outside scope.

Tools are unchanged from locally tested prototypes. USD liquidity adapter only; EPS and rate calculator require separately reviewed records; unsupported financial calculations need administrator-reviewed arithmetic. Read underlying code before execution. Private task records never enter Git. Requires Python 3.12 standard library only.
