# Make Money While You Sleep

## Reader resources for Using AI and Automations

Create a useful digital product, prepare a coherent multimedia demonstration, and inspect the work before publishing it. These resources accompany Juan Fernando Carpio's book. They are tools for doing the work, not evidence of income or a promise that a product will sell.

This is a private preparation copy. Public release and the license for reuse are pending the author's review. The book manuscript and unpublished business notes are not included here.

### Start here

Read [the quickstart](docs/QUICKSTART.md). For a route without automation software, open the completed [brief](examples/brief.json) and [review package](examples/review-package.json). Follow the structure using your own writing and design tools.

For the automation route, import the inactive n8n files in workflows/. Start with 01-product-studio in demo mode. It makes no provider calls. Read the source and draft side by side before connecting an AI model.

### What is included

- Product Studio: source brief to an article, spoken script, visual scenes, caption and editorial questions. The included demo is synthetic; local AI mode uses a separately configured Ollama installation.
- Local Multimedia Studio: approved text to portrait cards and an MP4, with optional owned narration. It saves a script, scene-timed draft subtitles and hashes in a manifest.
- Publication Review: checks a specific asset, destination and expiring approval. It deliberately contains no social publishing node.
- Unit Economics: calculates contribution and break-even from explicit assumptions. It does not estimate demand or revenue.
- PELE diagrams: editable Mermaid sources and exported SVG files for the business loop, studio, recovery path and economics.
- Practical templates: product brief, evidence ledger, offer outline, rights register and review checklist.

### What has been checked

See [VERIFICATION.md](docs/VERIFICATION.md). Executing the JavaScript logic locally does not prove import or execution inside n8n. A local silent video does not prove narration quality, AI-provider integration, checkout, delivery or a published social post.

No service accounts, customer data, API keys, account IDs or brand-private Notion content are included. Provider connections and purchases are not activated by importing these workflows.

### Keep your own copy

Download the repository and a release archive when the public edition is available. Keep your product sources and output files separately backed up. The essential process is also described in the book. No online host can honestly be promised to remain available forever.

### Requirements for the optional technical route

Node.js 20 or later; PELE 1.6.0 for rebuilding diagrams; Python 3.10 or later, Pillow, FFmpeg with libx264 and ffprobe for local video. n8n and an AI model are separate installations, not bundled products. Check their terms, availability and costs before using them.

The only JavaScript production dependency is PELE, licensed MIT by its maintainers. Rebuilding diagrams is optional; the exported SVGs can be read without installing it.
