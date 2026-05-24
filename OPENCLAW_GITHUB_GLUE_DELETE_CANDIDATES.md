# OpenClaw GitHub Glue Delete Candidates

## Context
Pi-native GitHub App auth + direct review writeback is now working from:
- `/root/.pi/agent/pr-review/extensions/pr-review-github-app-auth.ts`
- `/root/.pi/agent/pr-review/extensions/pr-review-github-writeback.ts`

Verified on live BYOQ PRs with `shawtics[bot]` authorship.

## Old OpenClaw-side GitHub helpers
These still exist under:
- `/root/.openclaw/workspace/tools/integrations/github/`

Files:
- `pr_context.py`
- `review_writeback.py`
- `writeback_result.py`
- `fix_comment_summary.py`

## Classification

### Likely deletable soon
- `/root/.openclaw/workspace/tools/integrations/github/review_writeback.py`

Reason:
- superseded by Pi-native direct REST writeback using GitHub App installation tokens

### Keep for now until usage sweep
- `/root/.openclaw/workspace/tools/integrations/github/pr_context.py`
- `/root/.openclaw/workspace/tools/integrations/github/writeback_result.py`
- `/root/.openclaw/workspace/tools/integrations/github/fix_comment_summary.py`

Reason:
- may still be referenced by older OpenClaw orchestration/reporting paths
- should not be deleted before a targeted reference sweep

## Recommended next step
1. sweep for references to the four Python helper files/classes/functions
2. if `review_writeback.py` is unreferenced or only referenced by legacy paths, delete it first
3. then evaluate the remaining three as a second batch
