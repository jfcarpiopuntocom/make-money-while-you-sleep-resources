"""AI engine room: a small local OpenAI-compatible router (default http://127.0.0.1:20129/v1).

It sends your routine text requests down a fallback chain of engines and returns the first answer that works.
- model "pool/text"       -> try each entry of "pool" in config.json, in order
- model "kobold/<x>"      -> your optional local KoboldCPP server ("kobold_url" in config.json)
- model "<name>/<model>"  -> an extra provider you declared under "providers" in config.json
- anything else           -> OmniRoute ("omniroute_url" in config.json)
Keys are read from environment variables whose NAMES you put in config.json; they are never printed or stored.
Listens on 127.0.0.1 only. Does not log prompts.
Usage: python router.py        (self-check: python router.py --check)"""
import json, os, sys, urllib.error, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))

def load_config(path=None):
    path = path or os.environ.get("AIE_CONFIG") or os.path.join(HERE, "config.json")
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except OSError:
        sys.exit(f"Missing {path}. Copy config.example.json to config.json and edit it.")

CFG = load_config() if __name__ == "__main__" and "--check" not in sys.argv else {}
OMNI = CFG.get("omniroute_url", "http://127.0.0.1:20128").rstrip("/")
KOBOLD = (CFG.get("kobold_url") or "").rstrip("/")
PROVIDERS = CFG.get("providers", {})
POOL = CFG.get("pool", [])
PORT = int(os.environ.get("ROUTER_PORT") or CFG.get("router_port", 20129))

def env_auth(var):
    key = os.environ.get(var, "").strip() if var else ""
    return {"Authorization": "Bearer " + key} if key else {}

def route(path, body, cfg=None):
    """Return (url, headers, body) for the requested model."""
    omni, kobold, providers = ((OMNI, KOBOLD, PROVIDERS) if cfg is None else
                               (cfg.get("omniroute_url", "").rstrip("/"), (cfg.get("kobold_url") or "").rstrip("/"), cfg.get("providers", {})))
    model = (body or {}).get("model") or ""
    head, _, rest = model.partition("/")
    if head == "kobold" and kobold:
        return kobold + path, {}, dict(body, model=rest)
    if head in providers:
        p = providers[head]
        return p["base_url"].rstrip("/") + path[len("/v1"):], env_auth(p.get("key_env")), dict(body, model=rest)
    return omni + path, env_auth((cfg or CFG).get("omniroute_key_env")), body

def call(method, url, hdr, body, timeout):
    req = urllib.request.Request(url, json.dumps(body).encode() if body is not None else None,
                                 {"Content-Type": "application/json", "User-Agent": "ai-engine-room", **hdr}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), r.headers.get("Content-Type", "application/json")

class H(BaseHTTPRequestHandler):
    def _send(self, code, data, ctype="application/json"):
        self.send_response(code); self.send_header("Content-Type", ctype); self.end_headers(); self.wfile.write(data)

    def _relay(self, method):
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0)) if method == "POST" else None
        body = json.loads(raw) if raw else None
        models = POOL if (body or {}).get("model") == "pool/text" else [(body or {}).get("model")]
        last = (502, json.dumps({"error": {"message": "router: no engine answered"}}).encode(), "application/json")
        for m in models:  # fallback chain: first engine that answers 200 wins
            if m and m.startswith("kobold/") and not KOBOLD:
                continue  # local engine not configured: skip it
            b = dict(body, model=m) if body is not None and m else body
            url, hdr, b = route(self.path, b)
            try:
                last = call(method, url, hdr, b, 120 if len(models) > 1 else 900)
                if last[0] == 200:
                    break
            except urllib.error.HTTPError as e:
                last = (e.code, e.read(), "application/json")
            except Exception as e:
                last = (502, json.dumps({"error": {"message": f"router: {m}: {type(e).__name__}"}}).encode(), "application/json")
        self._send(*last)

    def do_POST(self): self._relay("POST")
    def do_GET(self):
        if self.path == "/v1/models":
            try:
                omni = json.load(urllib.request.urlopen(urllib.request.Request(OMNI + "/v1/models", headers=env_auth(CFG.get("omniroute_key_env"))), timeout=20)).get("data", [])
            except Exception:
                omni = []
            extra = [{"id": "pool/text", "object": "model", "owned_by": "router"}]
            extra += [{"id": f"{n}/{m}", "object": "model", "owned_by": n} for n, p in PROVIDERS.items() for m in p.get("models", [])]
            if KOBOLD:
                extra.append({"id": "kobold/local", "object": "model", "owned_by": "koboldcpp"})
            return self._send(200, json.dumps({"object": "list", "data": omni + extra}).encode())
        self._relay("GET")
    def log_message(self, *a): pass  # no logs: prompts are never recorded

def self_check():
    cfg = {"omniroute_url": "http://127.0.0.1:1", "kobold_url": "http://127.0.0.1:2",
           "providers": {"acme": {"base_url": "https://example.test/v1", "key_env": "ACME_KEY"}}}
    chat = "/v1/chat/completions"
    assert route(chat, {"model": "gemini/x"}, cfg)[0] == "http://127.0.0.1:1" + chat
    assert route(chat, {"model": "kobold/local"}, cfg)[0] == "http://127.0.0.1:2" + chat
    url, _, b = route(chat, {"model": "acme/m1"}, cfg)
    assert url == "https://example.test/v1/chat/completions" and b["model"] == "m1"
    os.environ["ACME_KEY"] = "x"
    assert route(chat, {"model": "acme/m1"}, cfg)[1] == {"Authorization": "Bearer x"}
    print("router self-check OK")

if __name__ == "__main__":
    if "--check" in sys.argv:
        self_check()
    else:
        ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
