from pi_scraper_service.models import ArtifactKind, CaptchaProvider, CaptchaStrategy, VerificationMode


STRATEGIES: dict[CaptchaProvider, CaptchaStrategy] = {
    CaptchaProvider.HCAPTCHA: CaptchaStrategy(
        provider=CaptchaProvider.HCAPTCHA,
        display_name="hCaptcha",
        module_path="pi_scraper_service.extensions.hcaptcha",
        artifact_kind=ArtifactKind.TOKEN,
        verification_mode=VerificationMode.HTTP_POST,
        metadata_keys=["expected_selector", "form_action", "aspnet_fields"],
        inspiration_paths=[
            "captcha-solver/worker/solvers/hcaptcha.py",
            "captcha-solver/tests/test_hcaptcha.py",
        ],
        solve_hints=[
            "Some targets accept the same answer in both g-recaptcha-response and h-captcha-response.",
            "Preserve ASP.NET hidden fields when submitting solved tokens.",
        ],
    ),
    CaptchaProvider.RECAPTCHA_V2: CaptchaStrategy(
        provider=CaptchaProvider.RECAPTCHA_V2,
        display_name="reCAPTCHA v2",
        module_path="pi_scraper_service.extensions.recaptcha_v2",
        artifact_kind=ArtifactKind.TOKEN,
        verification_mode=VerificationMode.DOM_SUBMIT,
        metadata_keys=["request_verification_token", "verification_endpoint", "query_value"],
        inspiration_paths=[
            "captcha-solver/worker/solvers/recaptcha_v2.py",
            "captcha-solver/tests/test_recaptcha_v2.py",
        ],
        solve_hints=[
            "Inject g-recaptcha-response before submit when the target expects browser-side form submission.",
            "Some targets validate by raw HTTP POST rather than navigation.",
        ],
    ),
    CaptchaProvider.RECAPTCHA_V2_ENTERPRISE: CaptchaStrategy(
        provider=CaptchaProvider.RECAPTCHA_V2_ENTERPRISE,
        display_name="reCAPTCHA v2 Enterprise",
        module_path="pi_scraper_service.extensions.recaptcha_v2_enterprise",
        artifact_kind=ArtifactKind.TOKEN,
        verification_mode=VerificationMode.API_VERIFY,
        metadata_keys=["verification_endpoint", "csrf_field", "request_verification_token"],
        inspiration_paths=[
            "captcha-solver/worker/solvers/recaptcha_v2.py",
            "captcha-solver/tests/test_recaptcha_v2.py",
        ],
        solve_hints=[
            "Enterprise targets often expose a dedicated captcha verification endpoint.",
        ],
    ),
    CaptchaProvider.RECAPTCHA_V3: CaptchaStrategy(
        provider=CaptchaProvider.RECAPTCHA_V3,
        display_name="reCAPTCHA v3",
        module_path="pi_scraper_service.extensions.recaptcha_v3",
        artifact_kind=ArtifactKind.TOKEN,
        verification_mode=VerificationMode.API_VERIFY,
        metadata_keys=["page_action", "hidden_token_field", "verification_endpoint"],
        inspiration_paths=[
            "captcha-solver/worker/solvers/recaptcha_v3.py",
            "captcha-solver/tests/test_recaptcha_v3.py",
        ],
        solve_hints=[
            "Respect the pageAction associated with the target flow.",
            "Some targets require hidden field injection, others direct fetch/API verification.",
        ],
    ),
    CaptchaProvider.TURNSTILE: CaptchaStrategy(
        provider=CaptchaProvider.TURNSTILE,
        display_name="Cloudflare Turnstile",
        module_path="pi_scraper_service.extensions.turnstile",
        artifact_kind=ArtifactKind.TOKEN,
        verification_mode=VerificationMode.DOM_SUBMIT,
        metadata_keys=["turnstile_field", "callback_name"],
        inspiration_paths=[],
        solve_hints=[
            "Look for cf-turnstile-response fields and callback-based token handoff.",
        ],
    ),
    CaptchaProvider.DATADOME: CaptchaStrategy(
        provider=CaptchaProvider.DATADOME,
        display_name="DataDome slider",
        module_path="pi_scraper_service.extensions.datadome",
        artifact_kind=ArtifactKind.COOKIE,
        verification_mode=VerificationMode.COOKIE_REPLAY,
        metadata_keys=["proxy", "user_agent", "captcha_url"],
        inspiration_paths=[
            "captcha-solver/worker/solvers/datadome.py",
            "captcha-solver/tests/test_datadome.py",
        ],
        solve_hints=[
            "Treat the solved artifact as a datadome cookie/session unlock.",
            "Preserve proxy and user-agent consistency across trigger, solve, and verify.",
        ],
    ),
    CaptchaProvider.IMAGE_TO_TEXT: CaptchaStrategy(
        provider=CaptchaProvider.IMAGE_TO_TEXT,
        display_name="image/audio to text captcha",
        module_path="pi_scraper_service.extensions.image_to_text",
        artifact_kind=ArtifactKind.TEXT,
        verification_mode=VerificationMode.DOM_SUBMIT,
        metadata_keys=["captcha_image_selector", "captcha_audio_selector", "answer_field_selector"],
        inspiration_paths=[
            "captcha-solver/worker/solvers/image_to_text.py",
            "captcha-solver/tests/test_image_to_text.py",
        ],
        solve_hints=[
            "Extract image bytes before solve and use audio as an optional fallback.",
        ],
    ),
    CaptchaProvider.CUSTOM: CaptchaStrategy(
        provider=CaptchaProvider.CUSTOM,
        display_name="custom captcha",
        module_path="pi_scraper_service.extensions.custom",
        artifact_kind=ArtifactKind.CUSTOM,
        verification_mode=VerificationMode.MANUAL,
        metadata_keys=["custom_flow", "custom_fields"],
        inspiration_paths=[],
        solve_hints=["Use the provided metadata to describe the site-specific solve path."],
    ),
}


def get_strategy(provider: CaptchaProvider) -> CaptchaStrategy:
    return STRATEGIES[provider]
