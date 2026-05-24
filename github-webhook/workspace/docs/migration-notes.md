# Migration Notes

## Reused directly from `~/.pi/agent/pr-review`

- `jsonl.ts`
- `pi-rpc-runner.ts`
- `proof-of-work.ts`
- `tracer.ts`
- `types.ts`
- `extensions/proof-of-work.ts`

## Left behind on purpose

- PR review runtime/orchestrator code
- GitHub App auth and writeback
- webhook signature handling
- repo startup profiles tied to byoq PR review
- browser smoke code aimed at PR validation

## Expected next work

1. clean the copied harness types/naming so they read as generic harness code rather than PR leftovers
2. define captcha task contracts more fully
3. build provider adapters and browser/runtime strategy
4. add a real end-to-end captcha task runner
5. add tests and smoke flows
