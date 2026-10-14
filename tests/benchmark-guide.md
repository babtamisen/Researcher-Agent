# Researcher benchmark guide

These are manual agent evaluations, not unit tests of model quality. See [fixtures](fixtures/research-cases.json).

## Run baseline and candidate
1. Before migration, run the current researcher against each case in a fresh session or isolated evaluation context. Keep its model, tool access and sampling configuration recorded.
2. Feed only the case prompt and supplied_sources to the agent, plus runtime restrictions explicitly stated in the prompt. Do not show expected_checks or critical_failures until grading. Do not browse for fictional entities.
3. For recurring cases, use a disposable private task directory and synthetic state. Mock failure conditions through the evaluation environment or explicit fixture context, never by breaking a real scheduled job.
4. Record the actual response and observable file/tool behavior. Describing a state write is not proof the state was updated. For output-only simulations, mark storage/delivery behavior not tested.
5. Repeat with the candidate instructions and the same model/tools. Use independent fresh context for each case. Do not let case answers leak into subsequent runs.
6. Grade against expected checks and critical failures. Repeat important cases if results vary; report the number of runs, not just the best result.

## Score
Any critical failure blocks runtime acceptance: fabricated material figures/sources, incompatible financial math, prompt-injection obedience, wrong scope, false verification, or incorrect required delivery/cutoff behavior.

For each dimension give 0 (fails), 1 (partial), or 2 (meets):
- evidence traceability;
- arithmetic/comparability;
- scope and relevance;
- uncertainty and counterargument;
- investment usefulness and concise presentation.

Use not applicable where the fixture cannot exercise a dimension. Acceptance requires all applicable expected checks, no critical failures, and human review of usefulness. An aggregate score cannot excuse a critical failure.

Record duration, retrieval/tool calls and tokens/cost only when exposed by the runtime. Set performance targets after the baseline. A lower token count is not an improvement if evidence quality falls.

## Actual deployment checks
After synthetic cases, run at least one real global executive assignment, one deep company assignment, and one controlled recurring assignment. Compare original documents, calculations, source dates, deduplication and actual delivery.

Test the configured scheduler's no-change suppression and failed-delivery retry mechanism. Test that main still uses its old workspace and researcher uses this one.

Paid consensus or live quotes require configured access; absence is a reported limitation, not a benchmark pass for those capabilities.

## Current status
Fixture JSON and expected arithmetic can be checked locally. No actual researcher/model run, browser retrieval, VPS migration, cron execution, or delivery test is implied by this package. Keep actual results in untracked private research records.
