import asyncio
import json
import sys

from pi_scraper_service.engine import CaptchaEngine
from pi_scraper_service.models import CaptchaTaskRequest


async def main() -> None:
    raw = sys.stdin.read()
    task = CaptchaTaskRequest.model_validate_json(raw)
    result = await CaptchaEngine().solve(task)
    sys.stdout.write(json.dumps(result.model_dump(), indent=2) + "\n")


if __name__ == "__main__":
    asyncio.run(main())
