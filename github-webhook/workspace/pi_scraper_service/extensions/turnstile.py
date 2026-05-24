from pi_scraper_service.extensions.common import build_blocked_result, build_extension_result
from pi_scraper_service.models import CaptchaStrategy, CaptchaTaskRequest, CaptchaTaskResult, ExtensionBuildResult, ImplementationStatus


IMPLEMENTATION_STATUS = ImplementationStatus.STUB


async def solve_task(task: CaptchaTaskRequest, strategy: CaptchaStrategy) -> CaptchaTaskResult:
    return await build_blocked_result(task, strategy, "Turnstile solver not implemented yet")


def build_extension(task: CaptchaTaskRequest, strategy: CaptchaStrategy) -> ExtensionBuildResult:
    return build_extension_result(strategy, IMPLEMENTATION_STATUS)
