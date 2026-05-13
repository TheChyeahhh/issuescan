from __future__ import annotations

import json
import re
import subprocess


# Matches: https://github.com/owner/repo/issues/123
_URL_RE = re.compile(r"github\.com/([^/]+/[^/]+)/issues/(\d+)")
# Matches: owner/repo#123
_SHORT_RE = re.compile(r"^([^#\s]+/[^#\s]+)#(\d+)$")


def parse_input(raw: str) -> tuple[str, str]:
    """Return (repo, issue_number) from a URL, short form, or bare number."""
    raw = raw.strip()

    m = _URL_RE.search(raw)
    if m:
        return m.group(1), m.group(2)

    m = _SHORT_RE.match(raw)
    if m:
        return m.group(1), m.group(2)

    raise ValueError(
        f"Cannot parse issue reference: {raw!r}\n"
        "Accepted formats:\n"
        "  https://github.com/owner/repo/issues/123\n"
        "  owner/repo#123"
    )


def fetch_issue(repo: str, number: str) -> dict:
    """Fetch issue data using the gh CLI."""
    cmd = [
        "gh", "issue", "view", number,
        "--repo", repo,
        "--json", "title,body,comments,labels,state,author,createdAt,url",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        err = result.stderr.strip()
        raise RuntimeError(
            f"gh CLI error: {err}\n"
            "Make sure you are authenticated: gh auth login"
        )

    return json.loads(result.stdout)


def build_prompt(issue: dict, repo: str) -> str:
    title = issue.get("title", "")
    body = issue.get("body", "") or "(no description)"
    labels = ", ".join(l["name"] for l in issue.get("labels", [])) or "none"
    state = issue.get("state", "")
    author = issue.get("author", {}).get("login", "unknown")
    url = issue.get("url", "")

    # Include up to 5 most recent comments for context
    comments = issue.get("comments", [])[:5]
    comments_text = ""
    if comments:
        parts = []
        for c in comments:
            login = c.get("author", {}).get("login", "user")
            body_c = (c.get("body") or "")[:500]
            parts.append(f"@{login}: {body_c}")
        comments_text = "\n\n".join(parts)

    return f"""You are a senior software engineer performing a structured issue triage.

Analyze the following GitHub issue and respond in this exact format:

## Summary
2-3 sentences describing the problem clearly for someone who hasn't read the issue.

## Root Cause
Your best assessment of WHY this is happening based on the information available. If not determinable, say so and explain what additional info would help.

## Severity
One of: LOW / MEDIUM / HIGH / CRITICAL
With a one-line justification.

## Fix Steps
Numbered list of concrete steps to resolve the issue. Include code snippets or commands where helpful.

## Effort Estimate
One of: Quick Fix (< 1hr) / Small (1–4hrs) / Medium (1–2 days) / Large (3+ days)
With a brief reason.

## Suggested Labels
Labels that should be applied if not already present (e.g. bug, enhancement, good first issue, needs-investigation).

---
Repository: {repo}
Issue URL: {url}
State: {state}
Author: @{author}
Labels: {labels}

Title: {title}

Description:
{body[:3000]}

{"Comments:" if comments_text else ""}
{comments_text[:2000]}"""
