import type { RepoStartupProfile } from "./pr-review-types";

export const REPO_STARTUP_PROFILES: Record<string, RepoStartupProfile[]> = {
  "byoq-inc/byoq": [
    {
      name: "trading-frontend",
      cwd: "trading/frontend",
      command: ["npm", "run", "dev", "--", "--hostname", "127.0.0.1", "--port", "3100"],
      port: 3100,
      healthUrls: ["http://127.0.0.1:3100"],
      matchPaths: ["trading/frontend/", "shared-frontend/"],
      installCommand: ["npm", "install"],
    },
    {
      name: "get-my-rez-frontend",
      cwd: "get-my-rez/frontend",
      command: ["npm", "run", "dev", "--", "--hostname", "127.0.0.1", "--port", "3101"],
      port: 3101,
      healthUrls: ["http://127.0.0.1:3101"],
      matchPaths: ["get-my-rez/frontend/", "shared-frontend/"],
      env: {
        SSO_API_URL: "http://127.0.0.1:8002",
        RESY_API_URL: "http://127.0.0.1:8001",
      },
      installCommand: ["npm", "install"],
    },
    {
      name: "admin-console",
      cwd: "admin-console/frontend",
      command: ["npm", "run", "dev", "--", "--hostname", "127.0.0.1", "--port", "3102"],
      port: 3102,
      healthUrls: ["http://127.0.0.1:3102"],
      matchPaths: ["admin-console/frontend/", "shared-frontend/"],
      installCommand: ["npm", "install"],
    },
    {
      name: "safewatch-site",
      cwd: "marketing-sites/safewatch",
      command: ["npm", "run", "dev", "--", "--hostname", "127.0.0.1", "--port", "3103"],
      port: 3103,
      healthUrls: ["http://127.0.0.1:3103"],
      matchPaths: ["marketing-sites/safewatch/", "shared-frontend/"],
      installCommand: ["npm", "install"],
    },
  ],
};
