# Complete the example before connecting accounts

## Route A with the tools you already use

1. Read examples/brief.json. It defines a meal-planning kit, the audience, the problem and a short owned source.
2. Read examples/review-package.json. Compare the article, script, scenes and caption with that source. Nothing in the example is a verified sales result.
3. Open the SVG diagrams in diagrams/. Copy templates/product-brief.md and replace the example with a problem you understand.
4. Make a complete product and demonstration in your normal tools. Use templates/review-checklist.md before sharing them.
5. Use examples/unit-economics.csv to examine costs. Replace the assumptions; do not treat them as a platform quotation.

This route does not require n8n, a local model, Python or any paid API.

## Route B with n8n

Use an existing n8n installation you control. Do not buy a hosted plan just to run this demo. Import workflows/01-product-studio.json using n8n's import-from-file menu. Imported files are inactive and have no schedule or public webhook.

Open Edit your brief. Leave mode as demo and job_id as meal-plan-demo for the first run. Execute the workflow manually. The true branch returns the included example; it does not call Ollama or a paid provider. Inspect Review package. The output must say AWAITING_EDITORIAL_REVIEW and approved:false.

For another product, replace the brief, use mode:local_ai, and configure the Local Ollama HTTP node with the address of your own Ollama service and the exact model name you have installed. Do not assume the example model is installed. The node posts JSON to /api/chat with streaming off. Test a small public source first. If the response is malformed or its scene text is too long, revise the prompt or output and try again; do not bypass the validation.

The local model path does not upload the source to a cloud AI provider. If you substitute an external endpoint, inspect its terms and data handling before sending material. This pack does not configure external credentials for you.

## Render the included local video

Install the optional runtime tools through their official channels if they are not already available: Python, Pillow, FFmpeg and ffprobe. These are software requirements, not services included in a book purchase. Install Pillow in a virtual environment appropriate to your operating system.

From the resource folder, run:

```text
python tools/media_studio.py --job examples/approved-demo-render.json
```

The renderer creates outputs/meal-plan-demo-video/. Open video.mp4, the three cards, script.txt, captions-draft.srt and manifest.json. The demonstration is a short silent portrait video. It does not include generated speech. Subtitle timing follows scenes, not individual spoken words.

The example's approved:true applies only to the supplied synthetic example. For your own content, review the exact script and scene text before making a render job. Compute script_sha256 from the exact UTF-8 script_text. Do not change the script after calculating the hash. Use a new job_id when you change approved content.

To add your own recorded narration, create an assets/ folder and place the audio there. Add narration_file with its relative filename to the job JSON. The video retains the scene-defined duration and pads shorter audio with silence; longer audio is cut at that duration. Adjust timing or narration and review the final result. The supplied SRT is a draft and may need rewriting to match speech.

## Optional n8n connection to the local renderer

Start the service on the same computer after setting READER_STUDIO_TOKEN to a long random local secret of at least 24 characters. Keep it out of files committed to Git. Run:

```text
python tools/media_studio.py --serve
```

The service listens only on 127.0.0.1:8765. In n8n, import workflow 02 and create a Header Auth credential named as you prefer. Its header is Authorization and its value is Bearer followed by your token. Select that credential in Local media studio. The token is not included in the exported workflow.

Replace the deliberate error in Approved render input with your reviewed render-job JSON. The example input node refuses to run until you do this; importing the workflow cannot silently approve your content. The node should return a single item with that JSON, following the return structure in workflow 01's input node.

Same-computer localhost works only when n8n can reach that loopback service. A cloud n8n account cannot access your computer's localhost. Docker also has a different network namespace. For this pack, use the direct local command if the service is not reachable. Do not expose the renderer through a public tunnel or bind it to all interfaces to avoid understanding the network boundary.

No automatic retry is configured for rendering. A request that times out may still be running locally. Inspect the job folder and manifest before retrying. A completed identical job is reusable; a changed job must get a new ID.

## Review before publication

Watch the exported MP4. Check readability, sound, timing, facts, permissions and the buyer-facing promise. Workflow 03 requires a final video hash, an exact destination and a future expiry for the explicit approval. A changed file or destination fails the check. The workflow ends at READY_FOR_MANUAL_PUBLICATION; it does not publish or send anything.

Use the intended platform's own reviewed publishing process. Keep its final URL or post ID with the manifest. Do not call a draft, a queued upload or a successful HTTP request a verified publication.

## Rebuild diagrams and inspect code

With Node.js installed, use your normal package manager to install the dependency pinned in package.json, then run:

```text
node tools/build-workflows.mjs
node tools/render-diagrams.mjs
node tools/create-demo.mjs
node --test tests/core.test.mjs
python tests/test_media.py
```

The exported workflows contain their Code-node logic. They do not require custom JavaScript modules inside n8n. The local tests exercise those snippets with a small mock execution interface; they do not start n8n or certify compatibility with every version.
