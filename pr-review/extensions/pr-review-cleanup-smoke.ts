import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { runWebhookPrReview, type WebhookEnvelope } from "./pr-review-orchestrator";

async function main(): Promise<void> {
  const artifactRoot = "/tmp/pi-webhook-review-artifacts";
  const sessionKey = "hook:github-pr-byoq-inc-byoq-237";
  const sessionSlug = sessionKey.replace(/[^a-zA-Z0-9_.-]+/g, "-");
  const sessionDir = join(artifactRoot, sessionSlug);
  const prDir = join(sessionDir, "byoq-inc-byoq-pr-237");

  mkdirSync(prDir, { recursive: true });
  writeFileSync(join(prDir, "result.json"), "{}\n", "utf8");

  const envelope: WebhookEnvelope = {
    message: "[Fri 2026-05-08 01:22 UTC] PR_REVIEW_PIPELINE: PR #237 closed on byoq-inc/byoq",
    sessionKey,
    idempotencyKey: "cleanup-smoke-1",
  };

  const result = await runWebhookPrReview(envelope, {
    repoRootResolver: () => "/tmp/byoq-pr237-6aqR",
    artifactRoot,
  });

  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
