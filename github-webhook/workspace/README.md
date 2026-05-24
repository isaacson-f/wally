# pi-scraper-service

Python repository for a captcha solving engine with browser automation.

## Goals

- keep Pi as the execution substrate where it helps
- build the solving engine in Python
- give each captcha family its own extension module
- use the old `captcha-solver` service as implementation inspiration without dragging its whole architecture forward

## Layout

- `pi_scraper_service/models.py` — typed task, strategy, and result contracts
- `pi_scraper_service/strategies.py` — provider-to-strategy mapping
- `pi_scraper_service/engine.py` — provider dispatch engine
- `pi_scraper_service/extensions/` — one module per captcha family
- `pi_scraper_service/runtime.py` — runtime settings
- `pi_scraper_service/cli.py` — stdin/stdout task runner
- `tests/` — Python tests
- `docs/` — architecture notes

## Captcha extension model

Each captcha family has its own module under `pi_scraper_service/extensions/`.

Current extension targets:
- `hcaptcha.py`
- `recaptcha_v2.py`
- `recaptcha_v2_enterprise.py`
- `recaptcha_v3.py`
- `turnstile.py`
- `datadome.py`
- `image_to_text.py`
- `custom.py`

The strategy layer tracks the important differences between families:
- artifact kind (`token`, `text`, `cookie`, `jwt`, `custom`)
- verification mode (`dom_submit`, `http_post`, `api_verify`, `cookie_replay`, `manual`)
- provider-specific metadata keys
- inspiration paths from the existing `captcha-solver` implementation

## Current state

This is a Python scaffold for the next phase. The per-provider modules are stubbed, but the repo is structured for real browser automation and solver implementations.
