import { readFileSync } from "node:fs";
import { runWebhookPrReview, type WebhookEnvelope } from "./extensions/pr-review-orchestrator";

function repoRootFor(repo: string): string {
  const mapping: Record<string, string> = {
    "byoq-inc/byoq": "/tmp/byoq-pr237-6aqR",
  };
  return mapping[repo] ?? mapping["byoq-inc/byoq"];
}

async function main(): Promise<void> {
  const envelopePath = process.argv[2];
  if (!envelopePath) {
    throw new Error("usage: tsx pr-review-webhook-entrypoint.ts <envelopePath>");
  }

  const envelope = JSON.parse(readFileSync(envelopePath, "utf8")) as WebhookEnvelope;
  const result = await runWebhookPrReview(envelope, {
    repoRootResolver: repoRootFor,
    artifactRoot: "/tmp/pi-webhook-review-artifacts",
    checkoutRoot: "/tmp/pi-webhook-checkouts",
  });

  process.stdout.write(JSON.stringify(result));
}

main().catch((error) => {
  console.error(error?.stack ?? String(error));
  process.exit(1);
});
