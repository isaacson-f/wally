import pytest

from pi_scraper_service.engine import CaptchaEngine
from pi_scraper_service.models import ArtifactKind, CaptchaChallengeTarget, CaptchaProvider, CaptchaTaskRequest, CaptchaTaskStatus, ImplementationStatus


@pytest.mark.asyncio
async def test_engine_routes_task_to_provider_extension() -> None:
    task = CaptchaTaskRequest(
        task_id="task-456",
        provider=CaptchaProvider.TURNSTILE,
        challenge=CaptchaChallengeTarget(url="https://example.com/captcha", site_key="site-key"),
    )
    result = await CaptchaEngine().solve(task)
    assert result.provider is CaptchaProvider.TURNSTILE
    assert result.artifact_kind is ArtifactKind.TOKEN
    assert result.status is CaptchaTaskStatus.BLOCKED
    assert result.blocker == "Turnstile solver not implemented yet"


def test_engine_reports_provider_implementation_status() -> None:
    status = CaptchaEngine().get_implementation_status(CaptchaProvider.DATADOME)
    assert status is ImplementationStatus.STUB


def test_engine_builds_extension_plan_for_stub_provider() -> None:
    task = CaptchaTaskRequest(
        task_id="task-789",
        provider=CaptchaProvider.RECAPTCHA_V2,
        challenge=CaptchaChallengeTarget(url="https://example.com/captcha", site_key="site-key"),
    )
    result = CaptchaEngine().build_extension(task)
    assert result.provider is CaptchaProvider.RECAPTCHA_V2
    assert result.implementation_status is ImplementationStatus.STUB
    assert result.status is CaptchaTaskStatus.BLOCKED
    assert result.next_steps[-1] == "Commit and push the extension changes on the working branch."
