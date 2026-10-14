# Manual migration, updates and rollback

## Preconditions
Use the OS account that owns the running OpenClaw instance, not automatically root. Confirm that the terminal's profile/state directory matches the service's environment. Keep the existing shared workspace in place.

These steps prepare a migration; no server settings were changed by creating this package.

## 1. Inspect the actual instance
Run safe read-only discovery:
```bash
openclaw --version
openclaw agents --help
openclaw agents list --bindings
openclaw config --help
openclaw gateway --help
openclaw cron --help
```

The supplied documentation snapshot also describes automations as a newer cron interface. Use the command exposed by the installed release; do not assume a newer schema or command exists on your server.

Privately establish:
- the actual configuration/profile path, possibly overridden by environment;
- the existing researcher ID, workspace, model, distinct agentDir and tool access;
- main's workspace and state directory;
- bindings and every scheduled assignment intended for researcher;
- service unit, owner, working environment, and supported reload procedure;
- scheduler no-change suppression and failed-delivery retry behavior.

Do not paste full config files, auth stores, environment dumps or session databases into chat. If sharing diagnostics, extract only relevant fields and redact tokens and private destinations. TOOLS.md cannot establish capabilities by itself.

If main and researcher reuse agentDir, resolve that state collision separately before migration; do not copy or overwrite session/auth databases.

## 2. Baseline and backup
Run benchmark cases using the old researcher first if you want an accuracy/cost comparison. Keep tools and model fixed between baseline and candidate.

Under a private directory outside Git, back up the actual configuration, shared workspace instruction files and any relevant context. Use restrictive permissions and verify the backup is readable before changing anything. Backups containing credentials must remain private; do not upload them.

Record the original researcher workspace path, model, agentDir, bindings, job definitions, and service activation method. Pause only the research jobs being migrated, if necessary to prevent concurrent runs; record their enabled status for restoration.

## 3. Prepare the checkout
Clone as described in [README](../README.md). Confirm AGENTS.md is at the checkout root.

Inspect reviewed contents and record the intended commit:
```bash
cd "$HOME/agents/researcher-workspace"
git status --short
git rev-parse HEAD
git ls-files
```

A new clone should have a clean worktree. Inspect any previously existing checkout before reuse. Confirm original config and state are outside the repository.

Selectively retain researcher-specific user preferences and identity, where useful, in private ignored USER.md/IDENTITY.md files. Do not copy main's identity or personal memory broadly. Keep AGENTS.md/SOUL.md specialized; TOOLS.md should describe only verified capabilities.

## 4. Change only the workspace
Use the installed release's supported UI, configuration editor or CLI to set the existing researcher's workspace to the absolute checkout path. Do not use agents add to recreate an existing researcher.

Preserve agent ID, agentDir, credentials, model and fallbacks, bindings, and job assignments. Do not change main's workspace or state. Only change a job's agent assignment if discovery shows it is wrong and the user has authorized the correction.

Validate configuration using the mechanism supported by the installed release before applying a reload. Do not paste a configuration fragment from a different release. On validation failure restore the saved configuration and investigate before resuming jobs.

## 5. Activate and smoke-test
Apply a reload/restart only if required by that installed version, with the actual service owner/unit. Do not guess a root versus user service.

Start a fresh researcher session and ask it to describe its current scope/depth rule using the workspace contract. Confirm the new workspace is actually loaded; an old session may still carry old context.

Run one real executive task on a non-PSE topic and one deep company task. Inspect original source links, compatible figures, calculations, date cutoffs, and uncertainty handling.

Confirm main still loads its old instructions and research routing still reaches researcher. Run a controlled recurring assignment in a test destination already authorized by the user; verify source failure, duplicate suppression and delivery retry without sending unsolicited test messages.

Resume only the paused jobs after checks pass. Report model/runtime benchmark results separately from package checks.

## 6. Reviewed updates and pinning
Keep the server checkout read-only to the agent where practical. An operator fetches and reviews updates.

Use a clean branch and fast-forward-only pulls as in README. Record the old commit before update. For a strictly pinned deployment, fetch, inspect the intended commit, and check it out detached; the operator supplies the reviewed actual commit hash:
```bash
git fetch origin
git show --stat REVIEWED_COMMIT
git diff HEAD REVIEWED_COMMIT -- AGENTS.md SOUL.md TOOLS.md references
git switch --detach REVIEWED_COMMIT
```

REVIEWED_COMMIT is an explicit example field, not an executable default. Verify it belongs to the expected repository history. Detached checkouts update by reviewing and switching to another commit rather than pulling on a branch. Do not discard a dirty worktree.

Instruction changes can affect behavior without a model change. Repeat affected benchmark cases and a fresh-session smoke test. Research state remains ignored and private; a Git checkout does not replace runtime records.

## 7. Rollback
For a failed first migration, restore the original researcher's workspace setting or verified configuration backup, validate it, and apply the release-required activation procedure. Keep both workspaces until checks complete. Restore paused jobs' original enabled status after successful rollback.

For a bad instruction update, use a reviewed clean checkout and switch to the recorded previous commit. Preserve untracked private records; do not run git clean -fdx or destructive reset commands. Validate in a fresh session.

Do not restore old cron history or session databases merely to roll back instructions. Their restoration is a separate state-recovery operation.

## Remaining prerequisites for live activation
Current installed version, actual sanitized researcher configuration, configured model, tool inventory and relevant cron definitions are needed to produce an exact configuration change. GitHub repository ownership/access must be established when it is created. Never supply private tokens in chat.

Documentation basis: user-supplied snapshot dated 14 October 2026, [agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) and [multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent). Installed-release help/configuration remains authoritative.

