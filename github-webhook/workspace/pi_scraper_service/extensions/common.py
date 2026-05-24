from pi_scraper_service.models import CaptchaEvidence, CaptchaStrategy, CaptchaTaskRequest, CaptchaTaskResult, CaptchaTaskStatus, ExtensionBuildPlan, ExtensionBuildResult, ImplementationStatus


async def build_blocked_result(
    task: CaptchaTaskRequest,
    strategy: CaptchaStrategy,
    blocker: str,
) -> CaptchaTaskResult:
    return CaptchaTaskResult(
        task_id=task.task_id,
        provider=task.provider,
        status=CaptchaTaskStatus.BLOCKED,
        artifact_kind=strategy.artifact_kind,
        verification_mode=strategy.verification_mode,
        challenge_url=task.challenge.url,
        blocker=blocker,
        summary=blocker,
        evidence=CaptchaEvidence(
            metadata_keys=strategy.metadata_keys,
            inspiration_paths=strategy.inspiration_paths,
            solve_hints=strategy.solve_hints,
        ),
    )


def build_extension_plan(
    strategy: CaptchaStrategy,
    implementation_status: ImplementationStatus,
) -> ExtensionBuildPlan:
    return ExtensionBuildPlan(
        provider=strategy.provider,
        module_path=strategy.module_path,
        implementation_status=implementation_status,
        next_steps=[
            "Inspect the target captcha flow and collect missing metadata.",
            "Implement or extend the provider module for this captcha family.",
            "Add or update provider-specific tests.",
            "Run pytest and mypy before committing.",
            "Commit and push the extension changes on the working branch.",
        ],
        files_to_update=[
            strategy.module_path.replace(".", "/") + ".py",
            "pi_scraper_service/strategies.py",
            "tests/",
        ],
    )


def build_extension_result(
    strategy: CaptchaStrategy,
    implementation_status: ImplementationStatus,
) -> ExtensionBuildResult:
    plan = build_extension_plan(strategy, implementation_status)
    return ExtensionBuildResult(
        provider=strategy.provider,
        implementation_status=implementation_status,
        status=CaptchaTaskStatus.BLOCKED,
        summary=f"{strategy.display_name} extension is {implementation_status.value} and must be implemented in-repo before solving.",
        next_steps=plan.next_steps,
    )
