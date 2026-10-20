# 🛡️ LLM Security Lab

A hands-on lab demonstrating **OWASP Top 10 for LLM Applications** vulnerabilities
and their fixes. Each lab is a small, runnable bot that shows one attack class —
how it breaks, and how to fix it.

Built for learning offensive AI security (AI red teaming). All bots run against a
local DeepSeek API key. **For education only — test only systems you own.**

## ⚠️ Disclaimer
These bots are **intentionally vulnerable**. Run them only in an isolated lab
environment, on systems you own or are authorized to test. API keys are loaded
from environment variables and never committed (see `.gitignore`).

## Labs

| # | Lab | OWASP | What it shows |
|---|-----|-------|---------------|
| 01 | Direct Prompt Injection | LLM01 | A secret in the system prompt, "protected" by an instruction. Modern models resist it. |
| 02 | Indirect Prompt Injection | LLM01 | Attack hidden inside a document the bot summarizes. |
| 03 | Excessive Agency (VULNERABLE) | LLM06 / LLM05 | Bot runs shell commands from model output → RCE. |
| 04 | Excessive Agency (FIXED) | LLM06 | Same bot, secured with an allowlist + `shell=False`. |

## Key finding

Modern LLMs (DeepSeek, GPT-4, Claude) **resist text-based prompt injection** well —
asking a bot to "reveal its secret" almost always fails.

The real vulnerabilities live in the **layers around the model**:
- the application **trusting model output** as a safe action (lab 03),
- giving the model **excessive privileges** (shell, DB, email),
- unsafe **output handling** (rendering as HTML/SQL/shell).

Lab 03 → 04 shows the single most important fix: **never execute model output
directly.** Let the model pick a *key* from an allowlist; the app runs a fixed,
pre-approved command with `shell=False`.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # add your DeepSeek key
export DEEPSEEK_API_KEY=your_key
python3 labs/01_direct_injection.py
```

## Writeup

See [`WRITEUP.md`](WRITEUP.md) for the full walkthrough: each attack, why it
succeeded or failed, and the defense-in-depth fix.
