from enum import Enum

from pydantic import BaseModel


class CaptchaProvider(str, Enum):
    HCAPTCHA = "hcaptcha"
    RECAPTCHA_V2 = "recaptcha_v2"
    RECAPTCHA_V2_ENTERPRISE = "recaptcha_v2_enterprise"
    RECAPTCHA_V3 = "recaptcha_v3"
    TURNSTILE = "turnstile"
    DATADOME = "datadome"
    IMAGE_TO_TEXT = "image_to_text"
    CUSTOM = "custom"


class ArtifactKind(str, Enum):
    TOKEN = "token"
    TEXT = "text"
    COOKIE = "cookie"
    JWT = "jwt"
    CUSTOM = "custom"


class VerificationMode(str, Enum):
    DOM_SUBMIT = "dom_submit"
    HTTP_POST = "http_post"
    API_VERIFY = "api_verify"
    COOKIE_REPLAY = "cookie_replay"
    MANUAL = "manual"


class CaptchaTaskStatus(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class ImplementationStatus(str, Enum):
    STUB = "stub"
    EXPERIMENTAL = "experimental"
    READY = "ready"


class CaptchaChallengeTarget(BaseModel):
    url: str
    site_key: str | None = None
    action: str | None = None


class CaptchaTaskRequest(BaseModel):
    task_id: str
    provider: CaptchaProvider
    challenge: CaptchaChallengeTarget
    metadata: dict[str, str] | None = None


class CaptchaEvidence(BaseModel):
    metadata_keys: list[str]
    inspiration_paths: list[str]
    solve_hints: list[str]


class CaptchaTaskResult(BaseModel):
    task_id: str
    provider: CaptchaProvider
    status: CaptchaTaskStatus
    artifact_kind: ArtifactKind
    verification_mode: VerificationMode
    challenge_url: str
    artifact: str | None = None
    blocker: str | None = None
    summary: str
    evidence: CaptchaEvidence


class CaptchaStrategy(BaseModel):
    provider: CaptchaProvider
    display_name: str
    module_path: str
    artifact_kind: ArtifactKind
    verification_mode: VerificationMode
    metadata_keys: list[str]
    inspiration_paths: list[str]
    solve_hints: list[str]


class ExtensionBuildPlan(BaseModel):
    provider: CaptchaProvider
    module_path: str
    implementation_status: ImplementationStatus
    next_steps: list[str]
    files_to_update: list[str]


class ExtensionBuildResult(BaseModel):
    provider: CaptchaProvider
    implementation_status: ImplementationStatus
    branch_name: str | None = None
    commit_message: str | None = None
    status: CaptchaTaskStatus
    summary: str
    next_steps: list[str]
