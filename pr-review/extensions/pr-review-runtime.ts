import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { createApiBrowserSmokeRunner, type ApiBrowserSurface } from "./pr-review-browser-api-runner";
import { runPrReviewExtension } from "./pr-review-extension";
import type { PrReviewExtensionInput, PrReviewExtensionResult } from "./pr-review-types";

const execFileAsync = promisify(execFile);

export interface PrReviewRuntimeOptions {
  repoRoot: string;
  artifactRoot: string;
  browserSurface?: ApiBrowserSurface;
}

export interface PrReviewRuntimeRunResult {
  artifactDir: string;
  result: PrReviewExtensionResult;
  resultPath: string;
}

async function ensureRepoReady(repoRoot: string, input: PrReviewExtensionInput): Promise<void> {
  await execFileAsync("git", ["rev-parse", "--is-inside-work-tree"], { cwd: repoRoot });
  if (input.headRef) {
    await execFileAsync("git", ["checkout", input.headRef], { cwd: repoRoot });
  }
}

export async function runPrReviewRuntime(
  input: PrReviewExtensionInput,
  options: PrReviewRuntimeOptions,
): Promise<PrReviewRuntimeRunResult> {
  const artifactDir = join(options.artifactRoot, `${input.repo.replace(/\//g, "-")}-pr-${input.pr}`);
  mkdirSync(artifactDir, { recursive: true });

  await ensureRepoReady(options.repoRoot, input);

  const browserRunner = options.browserSurface
    ? createApiBrowserSmokeRunner({
        surface: options.browserSurface,
        screenshotDir: artifactDir,
        filePrefix: `pr-${input.pr}`,
      })
    : undefined;

  const result = await runPrReviewExtension(input, options.repoRoot, browserRunner);
  const resultPath = join(artifactDir, "result.json");
  writeFileSync(resultPath, `${JSON.stringify(result, null, 2)}\n`, "utf8");

  return {
    artifactDir,
    result,
    resultPath,
  };
}
