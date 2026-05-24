# OpenClaw Delete Proposal

## Sweep result
I did a reference sweep for:
- `/root/.openclaw/workspace/gastown/pi-tracer`
- `gastown/pi-tracer`
- `/root/.openclaw/workspace`

Across:
- `/root/.pi`
- `/opt/github-webhook`
- `/etc/systemd/system`
- `/root/.openclaw/workspace`

Result:
- **No remaining references were found** to the old OpenClaw-hosted Pi review path.

## Safe-delete candidates (pending Frank approval)

### 1. Superseded Pi review code copy
Now replaced by `/root/.pi/agent/pr-review`.

Delete candidate:
- `/root/.openclaw/workspace/gastown/pi-tracer/`

Why it looks safe:
- Pi-owned copy exists and typechecked
- live webhook server was repointed away from workspace path
- reference sweep found no remaining path references

### 2. Pi-tracer fixtures and smoke artifacts
These look like generated test/smoke outputs and fixtures from the old workspace-based iteration cycle.

Delete candidates:
- `/root/.openclaw/workspace/.artifacts/pi-tracer-fixtures/`
- `/root/.openclaw/workspace/.artifacts/pi-tracer-smoke/`
- `/root/.openclaw/workspace/.logs/pi-tracer-smoke/`

Why they look safe:
- generated artifacts, logs, and fixtures
- tied to the old workspace-hosted pi-tracer path
- not referenced in the sweep

## Keep for now
Even though we are moving past OpenClaw, I recommend keeping these a bit longer:
- `/root/.openclaw/workspace/MEMORY.md`
- `/root/.openclaw/workspace/USER.md`
- `/root/.openclaw/workspace/memory/`
- `/root/.openclaw/workspace/docs/`
- `/root/.openclaw/workspace/tools/docs/`
- broader `/root/.openclaw/workspace/gastown/` notes outside `pi-tracer/`

Reason:
- already copied/imported, but still useful as migration-era source/reference until Pi-native docs are curated further

## Recommended deletion order
1. delete workspace `gastown/pi-tracer/`
2. delete old pi-tracer fixtures/smoke/log artifacts
3. keep the rest of OpenClaw around as read-only reference until a later cleanup pass

## Awaiting approval
Do **not** delete until Frank explicitly confirms.
