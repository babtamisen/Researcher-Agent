# Executive and recurring briefing workflow

## Research
1. Read the task's question, scope, cutoff, timezone, depth and delivery instruction. Apply the [task contract](task-contract.md).
2. For a recurring job, inspect its own successful state; derive the review window. Check sources for revisions and newly released information. Old events recirculated today are not necessarily new catalysts.
3. Start with original releases and the prior evidence cache. Recheck release pages and revision status for fresh reporting; a saved source is not proof that nothing changed.
4. Rank developments by relevance to the assignment and investment significance. Include enough evidence to explain the change; omit peripheral news.
5. Use the relevant [verification checks](verification.md). Check a credible counterargument and avoid treating every development as price-sensitive.

## Output
Normally 300–600 words excluding sources, shorter for a narrow update. Respect the assignment's limit.
- As of: timestamp/timezone and reporting window when time-sensitive.
- Key takeaway: one short paragraph answering the question, including the central caveat.
- Material changes: verified figures and compatible comparisons.
- Implications: causal mechanisms, likely exposures, relevant horizon, and what remains inference.
- Risks/counterargument: the most consequential uncertainty or alternative.
- Next catalysts: known dated releases or events; do not invent a calendar.
- Sources/gaps: citations near claims, a compact list, and inaccessible or missing material evidence.

Do not fill every heading if the assignment only needs a narrow update. Separate management guidance, identifiable consensus and your own forecast. Without supported expectations or price context, do not claim a surprise or say the news is already priced in.

Example skeleton:
"As of [actual timestamp]. [Conclusion and qualification.]
[Verified change and comparison.] [Source]
[Implication and mechanism, labeled as inference where needed.]
[Counterargument or risk.] [Next verified catalyst.]
[Sources and any gaps.]"

## Recurring decisions
Use source URL, release identity, reporting period and substantive revision to detect new material.
- Verified no change: use configured behavior. Return a short no-update report if required.
- Notification-only task: use the scheduler's documented suppression mechanism when no material update exists. Do not guess a magic suppression token. If unavailable, disclose that delivery configuration must handle suppression; do not promise silence.
- Incomplete source checks: report verification incomplete, naming what was checked and what failed. Do not say no news.
- New revision: report the changed basis even if the release URL was previously seen.
- Interrupted/failed run: preserve successful cutoff and seen items. A partial report must not erase the unreviewed interval.
- Do not update cutoff to completion time if sources were checked only through an earlier time. Use the actual review cutoff.

## Delivery and persistence
Save useful evidence only with available file access; write successful state per the task contract. Keep the report and delivery mode consistent with the assignment. Return output to scheduler-managed delivery without making a second messaging-tool send.

A scheduler send failure may occur after generation. The scheduler must manage retry/history; the agent must not infer delivery success. Do not assume changed state guarantees a failed notification will be retried. Confirm retry behavior during deployment.

