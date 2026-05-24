# Claude Sub-Agents

Prompt templates for specialized sub-agents live in `.claude/agents/`. Claude should automatically pick the best sub agent for different tasks.

| Agent | File | Purpose |
|-------|------|---------|
| Research | `research.md` | Documentation lookup, codebase exploration, API reference |
| Linting | `linting.md` | Dead code removal, convention enforcement, cleanup |
| Testing | `testing.md` | Write and run pytest tests, coverage gap analysis |
| Security | `security.md` | Vulnerability scanning, secrets detection, input validation audit |
| Code Review | `review.md` | Diff review against CLAUDE.md guidelines |

# Token Efficiency Rules

## Sub-Agent Discipline
- Delegate file exploration and verbose operations (test runs, log analysis) to subagents — their output stays contained, not added to main context.
- Pre-scope every subagent task fully: context, goal, files, constraints. One complete prompt beats five clarifying exchanges.
- Batch similar work into a single subagent session. Startup overhead is ~20k tokens — amortize it.

## Context Hygiene
- Don't reference files with @ unless actively needed — it embeds the entire file every turn.
- Reference files by path and explain when to read them: "For FooBarError, see `path/to/docs.md`."
- Use /clear between unrelated tasks. Use /compact with guidance at logical breakpoints.
- "Document & Clear" pattern: dump plan/progress to a .md file → /clear → new session reads the .md.

## Output Efficiency
- Suppress explanations when not asked: output code directly, skip preamble.
- Reference code by file path and line numbers instead of re-pasting.
- Keep responses focused on what changed and why, not what was already there.

# Code Standards

Read and strictly follow `.claude/skills/anti-slop.md` before writing ANY code.

- No comments in code unless the user asks for them
- No docstrings except when required by tooling
- Self-documenting function and variable names
- If it needs a comment to be understood, rewrite it to be clearer
- Strict typing (TypeScript strict mode, Python mypy strict)
- No `Any`/`any` types
- Minimal imports (no wildcards, no unused)

# Project Guidelines

- Type hints are required for all function signatures.
- Prefer composition over inheritance.
- Keep functions small and focused on a single task.

## Python Standards

- Use `ruff` for linting
- Use `mypy` in strict mode
- Use `vulture` for dead code detection

## TypeScript Standards

- Use strict mode
- Explicit return types
- ESLint with strict rules
- No unused variables/imports

## File Organization

- Functions belong in domain-specific modules
- Keep modules small and focused

# Anti-Slop Guidelines

## Style

- No emojis anywhere in code, comments, or output.
- No excessive blank lines or decorative separators.

## Logging

- Only log critical errors and important state changes.
- No debug logging in production code.
- No verbose "Starting X..." / "Finished X" log spam.

## Over-Engineering

- Don't add features, refactor code, or make "improvements" beyond what was asked.
- A bug fix doesn't need surrounding code cleaned up.
- A simple feature doesn't need extra configurability.
- Don't create abstractions for things that are only used once.

## Backwards Compatibility

- Don't preserve backwards compatibility unless explicitly requested.
- Rewriting and replacing is preferred over shimming old behavior.
- Don't add deprecation warnings for code you're changing - just change it.
- Don't keep old function signatures "just in case".

## Defensive Coding

- Don't add error handling for scenarios that can't happen.
- Trust internal code and framework guarantees.
- Only validate at system boundaries (user input, external APIs).
- Validate through type boundaries not isinstance.

## Unnecessary Abstractions

- Don't create helpers, utilities, or wrapper functions for one-time operations.
- Don't extract constants for values used once.
- Don't create config options for things that won't change.
- Don't design for hypothetical future requirements.
