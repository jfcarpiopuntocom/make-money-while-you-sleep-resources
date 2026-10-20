"""llm: hand a routine text task to your free engines (via the local router) and print only the answer.
Good for summaries, drafts, extraction, classification and rewriting. Never send private or client data.
Usage:  python llm.py "instruction"                 (short prompt)
        python llm.py "instruction" file.txt        (appends the file's contents)
        echo text | python llm.py "instruction" -   (reads stdin)
Optional environment variables: LLM_MODEL (default pool/text), LLM_MAX_TOKENS (default 4000),
LLM_ROUTER_URL (default http://127.0.0.1:<router_port from config.json>)."""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

def router_url():
    if os.environ.get("LLM_ROUTER_URL"):
        return os.environ["LLM_ROUTER_URL"].rstrip("/")
    port = 20129
    try:
        with open(os.path.join(HERE, "config.json"), encoding="utf-8-sig") as f:
            port = int(json.load(f).get("router_port", port))
    except (OSError, ValueError):
        pass
    return f"http://127.0.0.1:{port}"

def build_body(prompt, model=None, max_tokens=None):
    return {"model": model or os.environ.get("LLM_MODEL", "pool/text"), "stream": False,
            "max_tokens": int(max_tokens or os.environ.get("LLM_MAX_TOKENS", "4000")),
            "messages": [{"role": "user", "content": prompt}]}

assert build_body("hi", "m", 5) == {"model": "m", "stream": False, "max_tokens": 5,
                                    "messages": [{"role": "user", "content": "hi"}]}

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    prompt = sys.argv[1]
    if len(sys.argv) > 2:
        src = sys.stdin.read() if sys.argv[2] == "-" else open(sys.argv[2], encoding="utf-8").read()
        prompt += "\n\n" + src
    req = urllib.request.Request(router_url() + "/v1/chat/completions", json.dumps(build_body(prompt)).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        out = json.load(r)
    sys.stdout.reconfigure(encoding="utf-8")
    print(out["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
