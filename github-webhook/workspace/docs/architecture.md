# Architecture

## Intent

This repository separates the generic Pi harness from the captcha application layer.

## Layers

### 1. Harness core

Reusable runtime pieces:
- Pi RPC transport
- strict JSONL reader/writer
- bounded executor request model
- proof-of-work validation
- artifact/event/result writing

### 2. Pi extensions

Structured Pi tools that support the harness contract.

Current extension:
- `proof_of_work`

### 3. Captcha service

Captcha-domain logic:
- task request/result contract
- provider-specific solving flow
- challenge/session handling
- browser/runtime requirements

### 4. App entrypoints

Thin runners that wire runtime config + task input into the captcha service.

## Non-goals

Not part of this repo by default:
- PR review workflows
- GitHub webhook/writeback behavior
- byoq-specific service boot logic
- OpenClaw orchestration conventions

## Migration stance

Copy only reusable harness pieces. Rewrite domain behavior where needed.
