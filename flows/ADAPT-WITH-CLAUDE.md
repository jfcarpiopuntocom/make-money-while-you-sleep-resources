# Adapt Any Flow With Claude

Open Claude Code in your studio folder, put the flow file you want in the folder, and paste this.

```
I want to adapt an n8n workflow file for my business. Please act as a patient guide for a non-technical person.

Rules:
- Ask me one question at a time, in plain words. Explain any technical word.
- Never ask for passwords or API keys. If a step needs one, tell me where in n8n I type it myself.
- Do not send, publish, pay or delete anything. Propose first and wait for my "yes".
- Keep the original file. Save your changes as a new file with a clear name.

Steps:
1. Read the workflow file I name and explain in five plain sentences what it does.
2. Ask me about my business, my email tool, my store and where I keep my contacts.
3. List every placeholder that looks like {{YOUR_...}} and ask me what to put in each.
4. Propose the changes (names, texts, waits, tools). Wait for approval.
5. Make the new file. Check that it is valid JSON.
6. Give me a test plan using my own email address and a fake contact, with what I should see at each step.
7. End with a short checklist before I switch the flow on.

The file I want to adapt is: [FILE NAME]
```

Tip: if my tool is not Gmail or Google Sheets, say so. Claude can swap in a different step (for example Send Email by SMTP, or Airtable), but every swap must be tested with your own email first.
