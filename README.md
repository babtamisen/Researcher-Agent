# Researcher workspace 0.3 — integrated test candidate

Start with OPENCLAW-INSTRUCTIONS.txt. Not accepted for production.

Adds the unchanged prototype 0.1 calculator, a deterministic artifact renderer, and references/calculation-workflow.md to the prior workspace. Neither tool enforces Gateway finalization or delivery. No whole-report validation claim is justified.

Python 3.12 standard library only; no installation, credentials or elevated permissions. Local checks: python3 -m unittest discover -s tests -v. Only runtime instructions, references/ and scripts/ enter candidate runtime; tests and examples stay outside. Keep original workspace active outside supervised temporary testing.

Calculator supports USD EPS, strictly reconciled USD net debt, and quarterly/annualized rate conversion. Other calculations need separately traced tools and explicit scope labels. Exact renderer preserves supplied paragraphs and citations but cannot verify their truth. Numerical final statements and report rendering remain voluntary agent behavior; test actual terminal output.

See scripts/CALCULATOR.md for schema, rounding, limits and errors. See references/calculation-workflow.md for extraction, claim auditing, failure handling and artifact rendering. Run artifacts contain private research and stay outside Git. No repository or VPS updates have been made by creating this package.
