# Task contract and private records

## Resolve the assignment
Extract question/objective, entities or geography, asset class/sector where relevant, reporting period, cutoff and timezone, depth, length, source constraints, recurring task-key, no-change behavior, and authorized delivery mode. Fields may be inferred only where the context makes them clear; not every task needs every field.

Interactive: clarify only material missing details. Otherwise state the assumption.
Unattended: use configured scope/timezone. If essential scope is missing, return an incomplete-assignment notice with the missing fields. Do not substitute PSE coverage.

Default depth is executive; deep research requires an explicit request. Task length takes priority over the normal 300–600 word executive range.

## Example payloads
These are instruction templates, not installed cron jobs.

### Global market briefing
"Prepare an executive briefing on US-listed semiconductor companies and their exposure to European demand. Cover material developments since the last successful run; use UTC. Task-key: us-semiconductor-demand. Maximum 500 words excluding sources. Include implications, counterarguments, and next catalysts. Return through the scheduler; no direct messaging. If no material change after successful checks, return a one-sentence no-update result."

### Company research
"Analyze the latest reported annual and quarterly results for the company and exchange specified in this request. Depth: deep. Assess segments, earnings quality, cash conversion, leverage, valuation inputs, and bull/base/bear scenarios. Separate published consensus from your own estimates. Use the specified reporting cutoff and cite original filings."

The company, exchange and cutoff must be supplied by the surrounding request; this template alone is not a complete unattended assignment.

### Trade data watch
"Check official nickel ore imports into Indonesia from the Philippines for the specified reporting month. Task-key: indonesia-nickel-imports. Compare with the same month last year and separately discuss weekly arrival estimates. Never mix arrivals and departures or overlapping windows. Use Asia/Manila. Notify only on material changes, through the configured scheduler destination. A failed official-source check requires a brief verification-incomplete notice."

## Evidence records
When persistence is warranted and file tools exist, store short JSONL records under research/tasks/<task-key>/evidence.jsonl. task-key must use only letters, digits, hyphens or underscores and must not contain path traversal, slashes or raw URLs. Choose a private one-off key for independent research.

Required fields: claim_id, claim, source_url, publisher, title, publication_date, retrieved_at, reporting_period, units, document_location, evidence_excerpt, status.
- publication_date: ISO date or null.
- retrieved_at: ISO 8601 timestamp with timezone.
- source_url: actual retrieved URL; null for unavailable evidence or synthetic fixtures.
- reporting_period, units, document_location: descriptive strings or null where not applicable.
- status: verified, conflicting, or unavailable. A verified input can still support a labeled inference.
- Keep excerpts short and relevant, respecting source usage limits.
- Optional calculation fields: inputs, formula, result. Preserve compatibility assumptions.
- Never record headers, tokens, passwords or unrelated private material.

## Recurring state
Path: research/tasks/<task-key>/state.json.
Fields: schema_version (1), task_key (string), last_successful_cutoff (ISO 8601 with timezone or null), seen_items (array of release identifiers).
A release identifier uses original source URL, release identity, reporting period and revision identity; a substantive revision must not be suppressed as an already-seen release.

On first run, use the configured lookback, or an explicit stated assumption if nonessential. Do not pretend a prior cutoff exists. Validate state shape and task-key before use. If corrupt, missing or mismatched, retain the old file, report degraded deduplication and use the assignment's lookback; do not silently discard history.

Prepare the next state privately and replace the successful state only after required work succeeds. Use an available atomic file-write mechanism when possible; never execute a guessed command just to update state. On failure, keep the previous cutoff/seen set. Prune very old seen items only when the task's retention policy allows it; never prune evidence needed for current comparisons.

For scheduler-managed delivery, report generation and scheduler delivery are separate: retain scheduler failure status for delivery retry, never claim confirmed delivery from generation alone. For agent-managed messaging, only mark required delivery complete after a tool confirms it.

Run different jobs with different keys. Avoid overlapping runs of the same key; these instructions are not a transactional database or locking service. If concurrency is required, add deterministic storage/locking before relying on it.

