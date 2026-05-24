import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { REPO_STARTUP_PROFILES } from "./pr-review-repo-profiles";
import { runBrowserSmoke, type BrowserSmokeRunner } from "./pr-review-browser-smoke";
import { runCurlProbe } from "./pr-review-curl-probe";
import { bootService, stopBootedService } from "./pr-review-service-boot";
import type {
  PrReviewEvidence,
  PrReviewExtensionInput,
  PrReviewExtensionResult,
  RepoDetectionResult,
  RepoStartupProfile,
} from "./pr-review-types";

const execFileAsync = promisify(execFile);

function emptyEvidence(): PrReviewEvidence {
  return { commands: [], urls: [], screenshots: [], artifacts: [], logs: [] };
}

async function gitChangedPaths(repoRoot: string, baseRef?: string, headRef?: string): Promise<string[]> {
  const range = baseRef && headRef ? `${baseRef}...${headRef}` : "HEAD~1...HEAD";
  const { stdout } = await execFileAsync("git", ["diff", "--name-only", range], { cwd: repoRoot });
  return stdout
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function detectSuggestedChecks(paths: string[]): string[] {
  const checks = new Set<string>();
  if (paths.some((path) => path.endsWith(".py") || path.includes("/tests") || path === "pyproject.toml")) {
    checks.add("pytest");
  }
  if (paths.some((path) => path.endsWith(".ts") || path.endsWith(".tsx") || path.endsWith("package.json"))) {
    checks.add("npm-test-or-build");
    checks.add("browser-smoke");
  }
  return [...checks];
}

function splitPathKinds(paths: string[]): Pick<RepoDetectionResult, "changedFrontendPaths" | "changedBackendPaths"> {
  const changedFrontendPaths = paths.filter((path) => /frontend|web|site|ui|components/.test(path));
  const changedBackendPaths = paths.filter((path) => !changedFrontendPaths.includes(path));
  return { changedFrontendPaths, changedBackendPaths };
}

async function detectRepo(repoRoot: string, repo: string, baseRef?: string, headRef?: string): Promise<RepoDetectionResult> {
  const changedPaths = await gitChangedPaths(repoRoot, baseRef, headRef);
  const profiles = (REPO_STARTUP_PROFILES[repo] ?? []).filter((profile: RepoStartupProfile) => {
    if (!profile.matchPaths?.length) return true;
    return changedPaths.some((path) => profile.matchPaths?.some((prefix: string) => path.startsWith(prefix)));
  });
  const split = splitPathKinds(changedPaths);
  return {
    repoRoot,
    profiles,
    changedFrontendPaths: split.changedFrontendPaths,
    changedBackendPaths: split.changedBackendPaths,
    suggestedChecks: detectSuggestedChecks(changedPaths),
  };
}

function formatCommand(command: string[]): string {
  return command.join(" ");
}

function resolveProfiles(detection: RepoDetectionResult): RepoStartupProfile[] {
  if (detection.profiles.length > 0) return detection.profiles;

  const fallbackProfiles: RepoStartupProfile[] = [];
  const packageJsonPaths = [
    "package.json",
    "frontend/package.json",
    "web/package.json",
  ];

  for (const relPath of packageJsonPaths) {
    const fullPath = join(detection.repoRoot, relPath);
    if (existsSync(fullPath)) {
      fallbackProfiles.push({
        name: `heuristic-${relPath.replace(/\//g, "-")}`,
        cwd: relPath.replace(/\/package\.json$/, ""),
        command: ["npm", "run", "dev"],
        healthUrls: ["http://127.0.0.1:3000/"],
      });
    }
  }

  return fallbackProfiles;
}

export async function runPrReviewExtension(
  input: PrReviewExtensionInput,
  repoRoot: string,
  browserRunner?: BrowserSmokeRunner,
): Promise<PrReviewExtensionResult> {
  const evidence = emptyEvidence();
  const detection = await detectRepo(repoRoot, input.repo, input.baseRef, input.headRef);
  const startupProfiles = resolveProfiles(detection);

  const findings = [];
  findings.push({
    severity: "info" as const,
    summary: `Detected ${detection.changedFrontendPaths.length} frontend paths and ${detection.changedBackendPaths.length} other changed paths`,
  });

  const readinessNotes: string[] = [];
  let bootedCount = 0;

  for (const profile of startupProfiles) {
    evidence.commands.push(formatCommand(profile.command));
    if (profile.healthUrls) {
      evidence.urls.push(...profile.healthUrls);
    }

    const boot = await bootService(repoRoot, profile).catch((error: Error) => ({
      service: null,
      ready: false,
      readinessFailures: [error.message],
    }));

    if (!boot.service) {
      findings.push({
        severity: "warning" as const,
        summary: `Failed to start ${profile.name}`,
        details: boot.readinessFailures.join("; "),
      });
      continue;
    }

    if (boot.service.process.exitCode !== null && !boot.ready) {
      findings.push({
        severity: "error" as const,
        summary: `${profile.name} exited before readiness`,
        details: boot.readinessFailures.join("; "),
      });
      evidence.logs?.push(...boot.service.stdout.slice(-20), ...boot.service.stderr.slice(-20));
      continue;
    }

    try {
      if (boot.ready) {
        bootedCount += 1;
        readinessNotes.push(`${profile.name}: ready`);
        evidence.logs?.push(...boot.service.stdout.slice(-20), ...boot.service.stderr.slice(-20));

        for (const url of profile.healthUrls ?? []) {
          const probe = await runCurlProbe(url);
          if (!probe.ok) {
            findings.push({
              severity: "warning" as const,
              summary: `curl probe failed for ${profile.name}`,
              details: probe.error ?? `HTTP ${probe.statusCode}`,
            });
            continue;
          }

          const browserSmoke = await runBrowserSmoke(url, browserRunner);
          if (browserSmoke.ok && browserSmoke.screenshotPath) {
            evidence.screenshots.push(browserSmoke.screenshotPath);
          } else if (input.interaction?.allowBrowser) {
            findings.push({
              severity: "info" as const,
              summary: `browser smoke not available for ${profile.name}`,
              details: browserSmoke.error,
            });
          }
        }
      } else {
        findings.push({
          severity: "warning" as const,
          summary: `${profile.name} did not become ready`,
          details: boot.readinessFailures.join("; "),
        });
      }
    } finally {
      await stopBootedService(boot.service);
    }
  }

  const recommendation = detection.changedFrontendPaths.length > 0 ? "comment" : "approve";
  const bodyLines = [
    `Pi PR extension evaluated ${startupProfiles.length} startup profile(s).`,
    bootedCount > 0 ? `Ready services: ${bootedCount}` : "No services became ready.",
    readinessNotes.length > 0 ? readinessNotes.join(", ") : "",
    detection.suggestedChecks.length > 0
      ? `Suggested checks: ${detection.suggestedChecks.join(", ")}`
      : "No additional checks inferred.",
  ].filter(Boolean);

  return {
    status: startupProfiles.length > 0 ? "completed" : "blocked",
    summary:
      startupProfiles.length > 0
        ? `Prepared repo-aware validation run for ${input.repo}#${input.pr}`
        : `No startup profile found for ${input.repo}#${input.pr}`,
    findings,
    evidence,
    writeback: {
      recommendation,
      body: bodyLines.join("\n"),
    },
  };
}
