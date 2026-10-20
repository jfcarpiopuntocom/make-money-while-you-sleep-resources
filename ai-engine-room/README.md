# Your AI Engine Room

> **Optional, and not for day one.** You do not need this folder to follow the book. Come back to it after your studio, product and first flow work. It hands boring public chores (summaries, first drafts, sorting) to free AI services so your paid plan lasts longer. **Never send client or private data to free engines.**
>
> **Check the model names yourself.** The model IDs in `config.example.json` are placeholders. Free plans, limits and model names change often. Look up the current ID in each provider's own page or in your OmniRoute dashboard before you use it.
> If you get stuck, paste this README to Claude and say: "Help me set this up one step at a time, and explain every word."


A starter kit for readers of *Make Money While You Sleep (Using AI and Automations)* by J. F. Carpio.

## What it is

Your paid AI subscription is a precious resource. A lot of what you ask it to do is routine: summarize this, draft that, tidy this paragraph, sort these notes into categories. The engine room is a small set of tools that runs on your own computer and hands that routine work to free AI services, so your paid subscription is kept for the work that needs it.

It has four parts:

- **OmniRoute**, an open-source gateway that lets you connect several AI providers (free and paid) behind one local address.
- **A small router** (`router.py`) that offers one simple address and, when one engine is busy or out of quota, quietly tries the next one in a list you control. This list is called the *pool*.
- **An optional local model** running on your own machine through KoboldCPP, started only when your computer has enough free memory.
- **The `llm` command** (`llm.py`), which sends a task to the pool and prints only the answer.

A launcher (`start-ai.bat`) starts everything, makes a dated backup of OmniRoute's database, runs a real test and writes a log.

## What it saves, honestly

It can stretch your paid AI subscription, because routine work no longer uses it. That is all. It does not guarantee any income or any particular saving. Free tiers have daily limits, can be slow, change without notice, and vary in quality. Treat the results as drafts that you review.

## Requirements

- Windows 10 or 11
- Python 3 (from python.org; tick "Add Python to PATH" during installation)
- Node.js (from nodejs.org), needed to install OmniRoute
- A free account with at least one AI provider (see below)

## Install, step by step

1. **Install OmniRoute.** Follow the instructions on its project page: https://github.com/diegosouzapw/OmniRoute (checked October 2026). It is installed with Node.js and starts a local dashboard, normally at `http://127.0.0.1:20128`. Open that address in your browser to confirm.
2. **Copy this folder** anywhere you like, for example `Documents\ai-engine-room`.
3. **Create your configuration.** Copy `config.example.json` to `config.json`. (If you skip this, the launcher does it for you the first time.)
4. **Add at least one provider** in the OmniRoute dashboard (next section).
5. **Edit the pool** in `config.json` so it lists models you actually connected (see "Editing config.json").
6. **Double-click `start-ai.bat`.** It checks OmniRoute, starts the router, makes a backup, runs a test and prints what happened. The same text is saved in the `logs` folder next to it.

## Adding free providers

You create the accounts yourself, on each provider's own website, and you paste the keys into OmniRoute's dashboard (Providers, then Add, choose the provider, paste the key, save and test). Never paste a key into a chat, a document or an email.

Providers that have offered a free tier recently, in no particular order:

- Google AI Studio (Gemini): a recurring free quota per model, no card needed. Free-tier prompts may be used by Google to improve its products.
- Mistral (the "Experiment" plan): recurring free usage with low request rates; phone verification is required. Free-plan requests may be used for training.
- NVIDIA NIM (build.nvidia.com): developer access to many models at modest rates; phone verification is required and the terms limit it to prototyping and research.
- OpenRouter: models whose names end in `:free`, with small daily limits unless you buy credits.
- Groq: a free plan with per-model daily limits.
- Cloudflare Workers AI: a small free daily allowance, enough for short drafts.
- Cerebras: sources disagree about whether a no-card free trial is still offered. Check the provider's own page.
- Others (Together, Fireworks, Moonshot, Hugging Face, Z.ai) were found to require payment in practice. Cohere's trial keys are not allowed for commercial use.

**The provider landscape changes fast.** The notes above were checked in October 2026 and many figures came from secondary sources. Free tiers shrink, move behind payment or disappear. Check each provider's own pricing and terms page, and trust your account's dashboard over any list, including this one.

You may also use a provider that OmniRoute does not list: add it under `providers` in `config.json` (next section).

## Editing config.json

`config.json` is plain JSON, so it cannot hold comments. Here is what each field means:

| Field | Meaning |
|---|---|
| `router_port` | Port of the router. Default 20129. |
| `omniroute_url` | Where OmniRoute listens. Keep it on `127.0.0.1`. |
| `omniroute_key_env` | Optional. The *name* of an environment variable holding an OmniRoute client key, if you turned on key protection in OmniRoute. Leave empty otherwise. |
| `pool` | The fallback chain used by the model name `pool/text`. Tried in order; the first engine that answers wins. |
| `providers` | Optional extra OpenAI-compatible services. Each has a short name, a `base_url`, `key_env` (the *name* of the environment variable that holds the key, not the key itself) and a `models` list. Use them in the pool as `name/model-id`. |
| `kobold_url` | Optional local model, for example `http://127.0.0.1:5001`. Empty means no local model. |
| `launcher` | Settings for `start-ai.ps1`: `omniroute_command`, `omniroute_data_dir` (empty means `.omniroute` in your user folder), `backups_keep`, `kobold_exe`, `kobold_model`, `kobold_port`, `min_free_ram_gb`. |

**Pool entries** are model ids as OmniRoute shows them in its dashboard, usually `provider/model`. The ones in `config.example.json` are placeholders: replace them with models you have connected. Put your fastest, most generous engine first, and fragile or low-quota ones last. An entry that starts with `kobold/` is skipped if you have not set `kobold_url`.

**An extra provider** looks like this (the key itself lives in a Windows environment variable called `MY_PROVIDER_KEY`, set in System Properties, Environment Variables):

```json
"providers": {
  "myprovider": { "base_url": "https://api.example.com/v1", "key_env": "MY_PROVIDER_KEY", "models": ["some-model"] }
}
```

and you would add `"myprovider/some-model"` to `pool`.

**Optional local model.** Download KoboldCPP and a small GGUF model (a model of a few billion parameters, 4-bit, is a good start), set `kobold_exe`, `kobold_model` and `kobold_url` (`http://127.0.0.1:5001`), and add `"kobold/local"` to the pool. The launcher starts it only when at least `min_free_ram_gb` of memory is free. Use `start-ai.bat kobold` to force it, or `start-ai.bat no-kobold` to skip it.

## Using `llm`

Open a terminal in this folder:

```
python llm.py "Summarize this in five bullet points" notes.txt
python llm.py "Rewrite this in a friendlier tone" draft.txt
echo some text | python llm.py "Classify this as complaint, question or praise" -
```

Optional settings (environment variables): `LLM_MODEL` to ask for one specific model instead of the pool, `LLM_MAX_TOKENS` to limit the length of the answer. Running `python llm.py` with no arguments prints the usage.

Good uses: first drafts, summaries, reformatting, sorting, simple extraction. Poor uses: anything that needs exact figures, quotations, legal or medical judgment, or your best thinking. Review everything before you use it.

## Safety rules

1. **Never send client data, passwords, personal or confidential information to free tiers.** Free plans may log prompts and may use them to train models. Anything you send is out of your hands.
2. **Keep everything on `127.0.0.1`.** The router refuses to listen anywhere else. Do not forward these ports to the internet or your local network.
3. **Keep API keys out of files you share.** Keys go in OmniRoute's dashboard or in environment variables. `config.json` holds only the names of variables. Before you share a folder, a screenshot or a backup, check that no key appears in it. The OmniRoute backups contain your provider settings, so treat them as private.
4. **Respect each provider's terms.** Personal use with your own keys is different from reselling access. Read the terms of any free tier before using it for commercial work.
5. **The router does not record your prompts**, but OmniRoute and the providers may keep their own logs. Check their settings.

## Troubleshooting

- **The test says "no engine answered".** Open the OmniRoute dashboard and check that at least one provider is connected and that the model ids in your pool match what the dashboard shows.
- **A provider returns error 403.** The key was probably revoked or pasted wrongly. Create a new key on the provider's site and replace it.
- **A provider returns error 429.** You hit its rate limit. Wait, or move it lower in the pool.
- **Port already in use.** Another program uses 20129. Change `router_port` in `config.json` and run the launcher again.
- **"python" is not recognised.** Reinstall Python and tick "Add Python to PATH", then open a new terminal.
- **OmniRoute is not started by the launcher.** Set `launcher.omniroute_command` to the command that starts it on your machine, or start it yourself first.
- **No backup is made.** The launcher looks for `storage.sqlite` in `omniroute_data_dir`. If your OmniRoute keeps its data elsewhere, set that field.
- **Garbled characters in the log.** Open the log with a UTF-8 capable editor such as Notepad.

To check the router's logic without starting anything: `python router.py --check`.

## Files

`start-ai.bat` and `start-ai.ps1` launcher · `router.py` fallback router · `llm.py` the command · `config.example.json` template · `LICENSE` MIT

*Provider notes checked October 2026. Verify before you rely on them.*
