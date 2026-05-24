# OpenClaw → Pi Migration Inventory

## Goal
Move forward with Pi as the real home for code, docs, memory, and project-management artifacts while treating `/root/.openclaw/workspace` as legacy/migration source material.

## Already moved
- `pr-review` runtime stack → `/root/.pi/agent/pr-review`

## Must port

### 1. PR review design / migration docs
These are active design-source docs for the system we just built and should live under Pi-owned docs.

Source files:
- `/root/.openclaw/workspace/pi-native-assistant-migration.md`
- `/root/.openclaw/workspace/pi-pr-extension-design.md`
- `/root/.openclaw/workspace/pi-tracer-spec.md`
- `/root/.openclaw/workspace/pi-tracer-review-summary.md`
- `/root/.openclaw/workspace/pi-tracer-skeleton-plan.md`
- `/root/.openclaw/workspace/docs/openclaw-pr-review-orchestration.md`
- `/root/.openclaw/workspace/tools/docs/architecture/pr-review-orchestration.md`

Recommended destination:
- `/root/.pi/agent/docs/pr-review/`

### 2. Gastown / Pi architecture notes
These still look like live architecture inputs rather than dead history.

Source files:
- `/root/.openclaw/workspace/gastown-phase-0-contract.md`
- `/root/.openclaw/workspace/gastown-pi-integration-assumptions.md`
- `/root/.openclaw/workspace/gastown-pi-layering-architecture.md`

Recommended destination:
- `/root/.pi/agent/docs/architecture/`

### 3. Durable project-management / memory material
If Pi is replacing OpenClaw as the operator surface, the important memory/docs should stop living only in `.openclaw/workspace`.

Source trees/files:
- `/root/.openclaw/workspace/MEMORY.md`
- `/root/.openclaw/workspace/USER.md`
- `/root/.openclaw/workspace/memory/`
- `/root/.openclaw/workspace/obsidian-vault/Shawty/memory`

Recommended destination:
- `/root/.pi/agent/memory/imported-openclaw/`
- then curate into:
  - `/root/.pi/agent/memory/hermes/`
  - Obsidian / project docs as appropriate

## Nice to port

### 4. Selected `gastown/` notes and prompt material
Need a smaller pass here; some of it is probably useful reference, some may be obsolete.

Candidate source tree:
- `/root/.openclaw/workspace/gastown/`

Recommended destination:
- `/root/.pi/agent/docs/gastown/`
- or `/root/.pi/agent/prompts/` for any still-live prompt/spec material

### 5. Memory tooling / dashboards
Potentially useful if you still want the dashboard behavior outside OpenClaw.

Source file:
- `/root/.openclaw/workspace/scripts/memory_dashboard.py`

Recommended destination:
- `/root/.pi/agent/tools/memory/`

## Leave for now

### 6. The old OpenClaw workspace repo itself
Leave intact until the docs/memory port is complete and verified.

Examples:
- `/root/.openclaw/workspace/gastown/pi-tracer/` (now superseded by `/root/.pi/agent/pr-review`)
- `.openclaw` config/persona files
- transcript capture files still serving as migration reference

## Delete later (after explicit confirmation)

### 7. Superseded PR-review code copy
Once verified that nothing still imports from it:
- `/root/.openclaw/workspace/gastown/pi-tracer/`

### 8. Pi-tracer smoke artifacts and fixtures
Likely disposable after confirming no active dependency:
- `/root/.openclaw/workspace/.artifacts/pi-tracer-fixtures/`
- `/root/.openclaw/workspace/.artifacts/pi-tracer-smoke/`
- `/root/.openclaw/workspace/.logs/pi-tracer-smoke/`

### 9. OpenClaw-specific scaffolding docs
After relevant content is ported elsewhere.

## Recommended next actions
1. Create Pi-owned docs folders:
   - `/root/.pi/agent/docs/pr-review/`
   - `/root/.pi/agent/docs/architecture/`
   - `/root/.pi/agent/docs/gastown/`
2. Copy the must-port docs into those locations.
3. Copy OpenClaw memory into a Pi-owned import area for curation.
4. Do a second pass to identify exact OpenClaw directories that are safe to delete.
5. Ask Frank for deletion confirmation before removing any OpenClaw files.

## Current deletion policy
Do **not** delete OpenClaw material yet without explicit confirmation.
