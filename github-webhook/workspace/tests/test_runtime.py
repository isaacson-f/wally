from pytest import MonkeyPatch

from pi_scraper_service.runtime import RuntimeSettings


def test_runtime_defaults_to_camoufox_browser(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("PI_SCRAPER_PLAYWRIGHT_BROWSER", raising=False)

    settings = RuntimeSettings()

    assert settings.playwright_browser == "camoufox"
