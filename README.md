# Small chat client (Week 2 lab)

A command-line program that sends one question to a model and prints the answer and the token usage. Python 3, standard library only — no packages.

## How to run it

Set the three environment variables (PowerShell shown; on bash use `export`):

```powershell
$env:CHAT_BASE_URL  = "https://openrouter.ai/api/v1"
$env:CHAT_MODEL     = "minimax/minimax-m3"
$env:OPENROUTER_API_KEY = "<your key>"
```

Then:

```bash
python chat.py "In one sentence, what is a context window?"
```

The program prints the model's one-line answer and then a final usage line of the form:

```
minimax/minimax-m3 in=185 out=122
```

## Intent corrections

Two things the agent had wrong or made up in its first draft of `intent/chat-client.md`:

1. **Not in scope** — the agent invented a long list (multi-turn, history, TUI, packaging, tests, …). Replaced with the assignment's short list: streaming, chat history, a web page, retries, more than one provider at a time.
2. **Success looks like** — the agent invented three specific behaviors (one-line answer, missing-env-var error handling, no secrets on disk). Replaced with the assignment's three observable outcomes: answers via OpenRouter, changing one environment variable points it at a different model, token counts match the provider's usage record.

## The request body in `chat.py`

The request body is built in `main()`:

```python
body = json.dumps({
    "model": model,
    "max_tokens": 600,
    "messages": [
        {"role": "system", "content": "Answer in pirate slang."},
        {"role": "user", "content": question},
    ],
}).encode("utf-8")
```

- `model` comes from `CHAT_MODEL`, so swapping the env var swaps the model with no code change.
- `max_tokens` caps how much the model can spend on the visible answer.
- `messages` carries the system prompt (sets the persona) and the user's question from `sys.argv[1]`.

## Two-model comparison

Same question — `"In one sentence, what is a context window?"` — under the pirate-slang system prompt.

| Model | in | out | Cost (Activity) | Behavior |
|---|---|---|---|---|
| `minimax/minimax-m3` | 185 | 122 | $0.000281 | Longer persona-driven answer with phrases like "Arrr, matey" and "trusty AI parrot." |
| `xiaomi/mimo-v2.5`   |  26 |  89 | $0.0000343 | Shorter answer, also pirate-themed but with different imagery ("treasure chest," "walk the plank"). |

Both models followed the system prompt's persona; the difference was length and which pirate metaphors they reached for. `xiaomi/mimo-v2.5` reported far fewer prompt tokens (26 vs 185) and cost roughly 8x less.

## Local model

Skipped — no local model was running on this machine during the lab, so the `Local model (optional)` row in `CHECKS.md` is marked N/A.
