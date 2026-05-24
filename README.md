# Wally

Wally is a Pi package/extension that gives agents and users a compact reference for the Pi `ExtensionAPI` object — the `pi` object passed to extension factories — plus the most useful context helpers.

## Install

```bash
pi install git:github.com/isaacson-f/wally
```

Or from a checkout:

```bash
pi -e ./src/index.ts
```

## What it adds

- `/wally [filter]` slash command for humans.
- `wally_pi_reference` tool for agents.
- A small footer status hint when loaded in interactive mode.

## Examples

```text
/wally registerTool
/wally provider
```

Agents can call `wally_pi_reference` with:

```json
{ "format": "markdown", "filter": "setActiveTools" }
```

or:

```json
{ "format": "json" }
```

## Covered Pi object areas

- Events and inter-extension event bus
- Tool registration and active tool control
- Commands, shortcuts, flags, and message injection
- Session state helpers
- Model/provider registration and thinking-level control
- Message rendering and UI/context helpers

## Development

```bash
npm install
npm run typecheck
```
