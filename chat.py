"""Small chat client: one question in, one answer and token counts out."""

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: chat.py <question>", file=sys.stderr)
        return 2

    question = sys.argv[1]

    try:
        base_url = os.environ["CHAT_BASE_URL"]
        model = os.environ["CHAT_MODEL"]
        api_key = os.environ["OPENROUTER_API_KEY"]
    except KeyError as e:
        print(f"missing environment variable: {e.args[0]}", file=sys.stderr)
        return 1

    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": question}],
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"connection error: {e.reason}", file=sys.stderr)
        return 1

    answer = payload["choices"][0]["message"]["content"]
    model_route = payload.get("model", model)
    usage = payload.get("usage", {})
    in_tokens = usage.get("prompt_tokens", 0)
    out_tokens = usage.get("completion_tokens", 0)

    print(answer)
    print(f"{model_route} in={in_tokens} out={out_tokens}")
    return 0


if __name__ == "__main__":
    sys.exit(main())