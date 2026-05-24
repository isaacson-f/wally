# Skill Improvement Ideas

Curated observations that may become or improve Pi skills. Review periodically; promote stable repeated workflows into ~/.pi/agent/skills/.

## Pi skill self-improvement loop added

- date: 2026-05-05
- proposed_skill: skill-self-improvement
- evidence: Pi can now record reusable workflow observations in SKILL_IDEAS.md and promote stable workflows into draft skills with skill_create_draft.

## Richer web tools extension

- date: 2026-05-05
- proposed_skill: web-vnc-automation
- evidence: Created web-tools extension with Brave search, guarded fetch, Chrome DevTools automation, and VNC screenshot/click/type/key control for this VPS.

## Replication-agent no-go audit workflow

- date: 2026-05-06
- proposed_skill: replication-nogo-audit
- evidence: User asked to inspect a large replication-agent PR branch, enumerate state-coded no-go files, compare blocked states against working states, and summarize recurring captcha/proxy failure modes before implementing fixes. This is likely reusable for future corp/sor scraper remediation passes.

## Tmux child-agent orchestration to PR workflow

- date: 2026-05-06
- proposed_skill: tmux-child-agent-pr-orchestration
- evidence: User asked to spawn one tmux per child agent, monitor completion, validate/commit child worktrees, and create PRs as each finishes. The reusable workflow needs auth checks, per-worktree test/commit, and push/PR creation handling.

## Observability dashboard S3-safe local E2E benchmarking

- date: 2026-05-06
- proposed_skill: observability-dashboard-e2e
- evidence: This task needed measuring FastAPI dashboard endpoints without repeatedly hitting the production S3 bucket. A reusable workflow emerged: generate a representative file:// OBSERVABILITY_ROOT fixture, run uvicorn locally with DASHBOARD_AUTH and cache TTL, mint the obs_session cookie from auth.py, then curl API endpoints cold/cached while recording time_total.

## GitHub PR review comment webhook fixer workflow

- date: 2026-05-10
- proposed_skill: github-pr-review-fixer
- evidence: While handling a pull_request_review_comment.created /fix webhook, replying in-thread required the REST endpoint `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies`; omitting the PR number returned 404. This is reusable for automated PR fixer tasks.

## Signal bridge response verification workflow

- date: 2026-05-23
- proposed_skill: signal-bridge
- evidence: User asked to make Signal responses work and wait until a new message arrived. Workflow involved checking signal-cli daemon and signal-pi-bridge service, restricting allowed_senders, restarting the bridge, sending a JSON-RPC Signal test message, then waiting on JSON-RPC receive events for the target sender.

## Preflight GitHub write permissions before push

- date: 2026-05-24
- proposed_skill: github-push-preflight
- evidence: A repo clone and local implementation succeeded, but both git push and GitHub Git Data API writes failed with 403 because the configured gh token lacked repository contents write access despite gh repo view showing admin metadata. A reusable preflight should test contents/write permissions before doing full work when a task requires pushing.

