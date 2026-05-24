# Pi Guidance

Read this before making code changes in this repository.

## Core Rules

- Keep code terse and self-documenting.
- No comments or docstrings unless tooling requires them.
- Prefer small focused functions over broad helpers.
- Do not introduce abstractions without immediate use.
- Do not preserve backward compatibility unless explicitly asked.
- Do not invent fake solved artifacts, tokens, cookies, or verification results.
- If a captcha flow cannot be solved honestly, return blocked with the exact blocker.

## Typing

- Python typing is mandatory.
- Mypy runs in strict mode.
- Avoid `Any`.
- Keep Pydantic models precise and provider-specific.

## Captcha Architecture

- Each captcha family owns its own module under `pi_scraper_service/extensions/`.
- Do not collapse provider-specific logic into one giant solver.
- Keep the strategy mapping in `pi_scraper_service/strategies.py` aligned with real solver behavior.
- Model the solved artifact correctly per provider:
  - token
  - text
  - cookie
  - jwt
  - custom
- Model verification mode correctly per provider:
  - dom_submit
  - http_post
  - api_verify
  - cookie_replay
  - manual

## Source Of Truth

Use the old `captcha-solver` implementation for inspiration on real-world flows, especially:
- hcaptcha
- recaptcha_v2
- recaptcha_v2_enterprise
- recaptcha_v3
- datadome
- image_to_text

Port behavior deliberately. Do not cargo-cult old architecture.

## Validation

Before finishing:
- run `pytest`
- run `mypy pi_scraper_service tests`

Keep the repo ready for a real Python browser-automation solving engine.
