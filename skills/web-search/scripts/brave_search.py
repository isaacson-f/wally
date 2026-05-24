#!/usr/bin/env python3
"""Search the web with Brave Search API.

Auth order:
1. BRAVE_API_KEY environment variable
2. op read from BRAVE_API_KEY_OP_REF, default op://Shawty/BRAVE_API_KEY/credential

The API key is never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

DEFAULT_OP_REF = "op://Shawty/BRAVE_API_KEY/credential"
API_URL = "https://api.search.brave.com/res/v1/web/search"


def get_api_key() -> str:
    key = os.environ.get("BRAVE_API_KEY")
    if key:
        return key.strip()

    op_ref = os.environ.get("BRAVE_API_KEY_OP_REF", DEFAULT_OP_REF)
    try:
        result = subprocess.run(
            ["op", "read", op_ref],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        raise SystemExit("Missing BRAVE_API_KEY and 1Password CLI `op` is not installed.")
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        raise SystemExit(f"Could not read Brave API key from 1Password ref {op_ref!r}: {stderr}")

    key = result.stdout.strip()
    if not key:
        raise SystemExit(f"1Password ref {op_ref!r} returned an empty API key.")
    return key


def brave_search(args: argparse.Namespace) -> dict:
    params = {
        "q": args.query,
        "count": str(args.count),
    }
    optional = {
        "country": args.country,
        "search_lang": args.language,
        "ui_lang": args.ui_lang,
        "freshness": args.freshness,
    }
    params.update({k: v for k, v in optional.items() if v})

    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": get_api_key(),
            "User-Agent": "pi-web-search-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:2000]
        raise SystemExit(f"Brave Search HTTP {exc.code}: {body}")


def simplify(data: dict, limit: int) -> dict:
    web = data.get("web", {}) or {}
    results = []
    for item in (web.get("results") or [])[:limit]:
        results.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "age": item.get("age"),
                "language": item.get("language"),
                "profile": (item.get("profile") or {}).get("name"),
            }
        )
    return {
        "query": data.get("query", {}).get("original") or data.get("query", {}).get("altered") or None,
        "results": results,
        "result_count": len(results),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the web with Brave Search API.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--count", type=int, default=5, choices=range(1, 11), metavar="1-10")
    parser.add_argument("--country", default="US", help="2-letter country code, default US")
    parser.add_argument("--language", default="en", help="Search language code, default en")
    parser.add_argument("--ui-lang", default=None, help="UI language code, e.g. en-US")
    parser.add_argument("--freshness", choices=["pd", "pw", "pm", "py", "day", "week", "month", "year"], default=None)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--raw", action="store_true", help="Print full Brave JSON response")
    args = parser.parse_args()

    data = brave_search(args)
    output = data if args.raw else simplify(data, args.count)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
