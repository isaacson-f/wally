from pi_scraper_service.models import ArtifactKind, CaptchaChallengeTarget, CaptchaProvider, CaptchaTaskRequest, VerificationMode
from pi_scraper_service.strategies import get_strategy


def test_datadome_strategy_uses_cookie_replay() -> None:
    strategy = get_strategy(CaptchaProvider.DATADOME)
    assert strategy.artifact_kind is ArtifactKind.COOKIE
    assert strategy.verification_mode is VerificationMode.COOKIE_REPLAY
    assert "captcha-solver/tests/test_datadome.py" in strategy.inspiration_paths


def test_recaptcha_v3_strategy_requires_page_action_metadata() -> None:
    strategy = get_strategy(CaptchaProvider.RECAPTCHA_V3)
    assert "page_action" in strategy.metadata_keys
    assert strategy.verification_mode is VerificationMode.API_VERIFY


def test_task_request_keeps_provider_specific_shape() -> None:
    task = CaptchaTaskRequest(
        task_id="task-123",
        provider=CaptchaProvider.HCAPTCHA,
        challenge=CaptchaChallengeTarget(url="https://example.com", site_key="site-key"),
        metadata={"expected_selector": "captcha-root"},
    )
    assert task.provider is CaptchaProvider.HCAPTCHA
    assert task.challenge.site_key == "site-key"
