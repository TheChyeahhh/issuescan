# issuescan

> AI-powered GitHub issue summarizer. Instant triage for any issue — no more reading walls of text.

Paste a GitHub issue URL and get a structured breakdown in seconds: what the problem is, why it's happening, how to fix it, and how long it will take.

---

## What it does

Fetches a GitHub issue (title, description, comments, labels) and returns:

- **Summary** — clear 2-3 sentence problem description
- **Root Cause** — why it's happening
- **Severity** — LOW / MEDIUM / HIGH / CRITICAL
- **Fix Steps** — numbered, actionable steps with commands
- **Effort Estimate** — Quick Fix / Small / Medium / Large
- **Suggested Labels** — what should be tagged on this issue

---

## Demo

```bash
$ issuescan https://github.com/TheChyeahhh/devlog/issues/1
```

```text
──────────────────────────────── issuescan ────────────────────────────────────
  Repo:    TheChyeahhh/devlog
  Issue:   #1
  Backend: claude

  API key not loading from .env file on Windows
  Comments: 3

╭──────────────────── Issue Analysis  #1 · TheChyeahhh/devlog ─────────────────╮
│                                                                               │
│  ## Summary                                                                   │
│  Users on Windows report that the .env file is not being loaded...            │
│                                                                               │
│  ## Root Cause                                                                │
│  python-dotenv requires the .env file to be in the working directory...       │
│                                                                               │
│  ## Severity                                                                  │
│  MEDIUM — affects all Windows users on first run                              │
│                                                                               │
│  ## Fix Steps                                                                 │
│  1. Pass the dotenv path explicitly...                                        │
│                                                                               │
│  ## Effort Estimate                                                           │
│  Quick Fix (< 1hr) — single line change                                       │
│                                                                               │
│  ## Suggested Labels                                                          │
│  bug, windows, good first issue                                               │
│                                                                               │
╰───────────────────────────────────────────────────────────────────────────────╯
```

---

## Requirements

- **GitHub CLI (`gh`)** must be installed and authenticated
  - Install: `brew install gh` (Mac) or [cli.github.com](https://cli.github.com)
  - Authenticate: `gh auth login`
- Python 3.9+
- A [Claude API key](https://console.anthropic.com) or [OpenAI API key](https://platform.openai.com)

---

## Installation

**Mac / Linux:**

```bash
git clone https://github.com/TheChyeahhh/issuescan.git
cd issuescan
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Windows:**

```bash
git clone https://github.com/TheChyeahhh/issuescan.git
cd issuescan
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

---

## Setup

```bash
cp .env.example .env
```

Open `.env` and add your API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here
AI_BACKEND=claude
```

---

## Usage

```bash
# Full URL
issuescan https://github.com/owner/repo/issues/123

# Short form
issuescan owner/repo#123

# Use OpenAI instead of Claude
issuescan owner/repo#123 --backend openai
```

---

## Future Ideas

- `--comment` flag to post the analysis back as a GitHub comment
- `--batch` mode to scan all open issues in a repo
- Priority scoring across multiple issues
- Slack / Discord webhook output

---

## License

MIT
