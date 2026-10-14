# OpenClaw Researcher Workspace v0.2 candidate

A dedicated workspace for your existing researcher agent, with financial-analyst research standards and concise executive briefings by default. Market, geography, entities and monitoring scope come from each task or cron. Detailed reports are available when requested.

This is an instruction/workflow package, not a new model or autonomous data service. It does not include proprietary data subscriptions, deterministic storage/locking, or an automatic deployment process.

## Candidate status
This revision has not passed actual-agent acceptance. Read [v0.2 retest handoff](docs/v0.2-retest-handoff.md) before any workspace switch. Headless evaluation is ineligible for this OAuth setup. Validate interruption recovery first and restore the original workspace even after a passing retest.

## What is included
- [AGENTS.md](AGENTS.md): research operating contract.
- [SOUL.md](SOUL.md): independent analyst voice.
- [TOOLS.md](TOOLS.md): capability/access guidance.
- [Task contract](references/task-contract.md): assignments and private record schemas.
- [Briefing](references/briefing.md), [deep research](references/deep-research.md), and [verification](references/verification.md) workflows.
- [Benchmark guide](tests/benchmark-guide.md) and 16 synthetic cases.
- [Migration guide](docs/migration.md), including rollback.
- [Verification report](docs/verification-report.md): actual local checks and pending runtime evaluation.

## GitHub later: push from your computer
Extract the ZIP. Open a terminal inside the extracted researcher-workspace directory. Keep AGENTS.md at the repository root; do not put the entire package one extra directory beneath the root.

Requires Git and authorized access to your GitHub account. Create a new private, empty repository using GitHub's UI; do not initialize it with a README. Then run:

```bash
git init -b main
git add AGENTS.md SOUL.md TOOLS.md README.md .gitignore references tests docs
git status --short
git diff --cached --stat
git commit -m "Add researcher workspace v0.2"
git remote add origin https://github.com/YOUR_USERNAME/openclaw-researcher.git
git push -u origin main
```

Replace YOUR_USERNAME with your account and use your actual repository name. Use Git's credential manager or an SSH key; never put a token in a URL or this repository. Configure Git author name/email locally if Git requests them. Inspect staged contents before pushing; .gitignore is not a substitute for review.

The ZIP contains curated source files, not Git history. A later push initializes your own repository and author metadata.

## Pull onto your OpenClaw server
Run as the same OS account that owns the running OpenClaw instance. Private repository access requires that account's authorized Git credential or SSH key.

```bash
git clone https://github.com/YOUR_USERNAME/openclaw-researcher.git \
  "$HOME/agents/researcher-workspace"
```

If the destination already exists, inspect it and follow the migration guide; do not clone over it or delete it.

Then change the existing researcher's workspace to that checkout using your installed OpenClaw version's supported configuration mechanism. Preserve its agent ID, state directory, model, bindings, and jobs. The exact edit depends on the actual running configuration; no guessed JSON schema is included.

GitHub hosts the files; the server runs the agent using the local checkout. OpenClaw does not automatically pull GitHub because a workspace points at a repository.

## Later updates
From a reviewed, clean server checkout:
```bash
cd "$HOME/agents/researcher-workspace"
git status --short
git fetch origin
git log --oneline HEAD..origin/main
git diff HEAD..origin/main -- AGENTS.md SOUL.md TOOLS.md references docs tests
git pull --ff-only origin main
git rev-parse HEAD
```

Inspect changes before pulling; record the previous commit for rollback. If the checkout is dirty or has diverged, stop and reconcile it explicitly. Never use a hard reset to discard local changes casually. Activate/reload only as required by the installed OpenClaw release; start a fresh research session for the smoke check.

For strict version pinning, review and deploy an explicit commit using the migration guide. The agent must not update its own checkout.

## Usage
"Executive briefing on the latest relevant developments in the entities and market specified below, as of [your cutoff]. Include implications, risks, next catalysts and sources."

"Deep research on [company and exchange]: segment drivers, earnings quality, cash flow, leverage and supported valuation scenarios."

Supply actual scope in place of the example fields. Cron payloads additionally specify timezone, reporting window/task-key, no-change behavior and delivery mode; see the task contract. These examples do not create schedules.

## Permissions, privacy and limitations
The package adds no tool permissions. Reading/searching sources, executing calculations, private file writes and scheduled delivery depend on existing runtime configuration. Configuration changes require the OS account's access to OpenClaw files and service controls.

Keep private memory, research output, credentials and machine-specific context out of Git. Do not copy the main agent's workspace wholesale. A separate workspace does not enforce host-level isolation.

The startup instructions are compact and deeper references load when relevant. Runtime benchmarks are still required: local checks validate the package, not the model's research quality.

