from pi_scraper_service.extensions.custom import IMPLEMENTATION_STATUS as CUSTOM_STATUS
from pi_scraper_service.extensions.custom import build_extension as build_custom_extension
from pi_scraper_service.extensions.custom import solve_task as solve_custom_task
from pi_scraper_service.extensions.datadome import IMPLEMENTATION_STATUS as DATADOME_STATUS
from pi_scraper_service.extensions.datadome import build_extension as build_datadome_extension
from pi_scraper_service.extensions.datadome import solve_task as solve_datadome_task
from pi_scraper_service.extensions.hcaptcha import IMPLEMENTATION_STATUS as HCAPTCHA_STATUS
from pi_scraper_service.extensions.hcaptcha import build_extension as build_hcaptcha_extension
from pi_scraper_service.extensions.hcaptcha import solve_task as solve_hcaptcha_task
from pi_scraper_service.extensions.image_to_text import IMPLEMENTATION_STATUS as IMAGE_TO_TEXT_STATUS
from pi_scraper_service.extensions.image_to_text import build_extension as build_image_to_text_extension
from pi_scraper_service.extensions.image_to_text import solve_task as solve_image_to_text_task
from pi_scraper_service.extensions.recaptcha_v2 import IMPLEMENTATION_STATUS as RECAPTCHA_V2_STATUS
from pi_scraper_service.extensions.recaptcha_v2 import build_extension as build_recaptcha_v2_extension
from pi_scraper_service.extensions.recaptcha_v2 import solve_task as solve_recaptcha_v2_task
from pi_scraper_service.extensions.recaptcha_v2_enterprise import IMPLEMENTATION_STATUS as RECAPTCHA_V2_ENTERPRISE_STATUS
from pi_scraper_service.extensions.recaptcha_v2_enterprise import build_extension as build_recaptcha_v2_enterprise_extension
from pi_scraper_service.extensions.recaptcha_v2_enterprise import solve_task as solve_recaptcha_v2_enterprise_task
from pi_scraper_service.extensions.recaptcha_v3 import IMPLEMENTATION_STATUS as RECAPTCHA_V3_STATUS
from pi_scraper_service.extensions.recaptcha_v3 import build_extension as build_recaptcha_v3_extension
from pi_scraper_service.extensions.recaptcha_v3 import solve_task as solve_recaptcha_v3_task
from pi_scraper_service.extensions.turnstile import IMPLEMENTATION_STATUS as TURNSTILE_STATUS
from pi_scraper_service.extensions.turnstile import build_extension as build_turnstile_extension
from pi_scraper_service.extensions.turnstile import solve_task as solve_turnstile_task
from pi_scraper_service.models import CaptchaProvider, CaptchaTaskRequest, CaptchaTaskResult, ExtensionBuildResult, ImplementationStatus
from pi_scraper_service.strategies import get_strategy


SOLVER_BY_PROVIDER = {
    CaptchaProvider.HCAPTCHA: solve_hcaptcha_task,
    CaptchaProvider.RECAPTCHA_V2: solve_recaptcha_v2_task,
    CaptchaProvider.RECAPTCHA_V2_ENTERPRISE: solve_recaptcha_v2_enterprise_task,
    CaptchaProvider.RECAPTCHA_V3: solve_recaptcha_v3_task,
    CaptchaProvider.TURNSTILE: solve_turnstile_task,
    CaptchaProvider.DATADOME: solve_datadome_task,
    CaptchaProvider.IMAGE_TO_TEXT: solve_image_to_text_task,
    CaptchaProvider.CUSTOM: solve_custom_task,
}

BUILD_EXTENSION_BY_PROVIDER = {
    CaptchaProvider.HCAPTCHA: build_hcaptcha_extension,
    CaptchaProvider.RECAPTCHA_V2: build_recaptcha_v2_extension,
    CaptchaProvider.RECAPTCHA_V2_ENTERPRISE: build_recaptcha_v2_enterprise_extension,
    CaptchaProvider.RECAPTCHA_V3: build_recaptcha_v3_extension,
    CaptchaProvider.TURNSTILE: build_turnstile_extension,
    CaptchaProvider.DATADOME: build_datadome_extension,
    CaptchaProvider.IMAGE_TO_TEXT: build_image_to_text_extension,
    CaptchaProvider.CUSTOM: build_custom_extension,
}

IMPLEMENTATION_STATUS_BY_PROVIDER = {
    CaptchaProvider.HCAPTCHA: HCAPTCHA_STATUS,
    CaptchaProvider.RECAPTCHA_V2: RECAPTCHA_V2_STATUS,
    CaptchaProvider.RECAPTCHA_V2_ENTERPRISE: RECAPTCHA_V2_ENTERPRISE_STATUS,
    CaptchaProvider.RECAPTCHA_V3: RECAPTCHA_V3_STATUS,
    CaptchaProvider.TURNSTILE: TURNSTILE_STATUS,
    CaptchaProvider.DATADOME: DATADOME_STATUS,
    CaptchaProvider.IMAGE_TO_TEXT: IMAGE_TO_TEXT_STATUS,
    CaptchaProvider.CUSTOM: CUSTOM_STATUS,
}


class CaptchaEngine:
    async def solve(self, task: CaptchaTaskRequest) -> CaptchaTaskResult:
        strategy = get_strategy(task.provider)
        solve_task = SOLVER_BY_PROVIDER[task.provider]
        return await solve_task(task, strategy)

    def get_implementation_status(self, provider: CaptchaProvider) -> ImplementationStatus:
        return IMPLEMENTATION_STATUS_BY_PROVIDER[provider]

    def build_extension(self, task: CaptchaTaskRequest) -> ExtensionBuildResult:
        strategy = get_strategy(task.provider)
        build_extension = BUILD_EXTENSION_BY_PROVIDER[task.provider]
        return build_extension(task, strategy)
