# Intent: small chat client

## Goal
A small command-line chat client. Running it with a question as an argument prints the model's answer, then a final line with the model name and the input/output token counts. No secrets in code, no third-party packages.

## Who it is for
The student running the week 2 introductory lab. Today the exercise is presumably done by hand or with sample code from the assignment sheet.

## Constraints
- Python 3, standard library only. No `pip install`, no third-party packages.
- Runs on Windows under PowerShell; HTTP calls go through `urllib.request`.
- Talks to an OpenAI-compatible chat-completions endpoint.
- Base URL, model name, and API key are read from environment variables:
  - `CHAT_BASE_URL` — endpoint root (e.g. `https://openrouter.ai/api/v1`)
  - `CHAT_MODEL` — model route (e.g. `minimax/minimax-m3`)
  - `OPENROUTER_API_KEY` — bearer token
- Nothing secret is hardcoded; the program fails clearly if any required variable is missing.
- The question is read from `sys.argv[1]`.

## Not in scope
- Streaming.
- Chat history.
- A web page.
- Retries.
- More than one provider at a time.

## Success looks like
- Answers a question through OpenRouter.
- Changing one environment variable points it at a different model.
- The token counts match the provider's usage record.

For example: `python chat.py "What is 2+2?"` prints a one-line answer and then a final line of the form `model in=N out=M`, where `model` is the route returned by the API and `N` and `M` are the prompt and completion token counts it reported. A missing required env var or a non-2xx response produces a readable error message and a non-zero exit code. The script requires no non-stdlib packages and writes no secrets to disk.

## Open questions
- If `CHAT_BASE_URL` or `CHAT_MODEL` is unset, should the program fail loudly or fall back to defaults (`https://openrouter.ai/api/v1`, `minimax/minimax-m3`)?
- Where should errors go — stderr or stdout — and what exit code on failure?
- Should the answer text be trimmed of leading/trailing whitespace before printing, or printed verbatim from the API?
- Exact final-line wording is confirmed as `model in=N out=M` with single spaces, but worth pinning in the spec.

**Approved by:** Nadia Boudhaim Maguire, Sept 26th, 2026