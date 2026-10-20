# The Flow Library (F1 to F8)

Eight ready-made automations for n8n. n8n is a free visual tool that works like an assembly line: something happens (a trigger), then a few steps run, then you get a result.

**Honest status.** These files are designed for you to adapt with your AI. They are valid n8n workflow files, but they have not been run on your setup, and the author ran only an email-campaign flow in production. Test each one with your own email address before you trust it. Nothing sends until you switch a flow on. Every flow ships switched off.

## How to import a flow
1. Open n8n. Click the three dots next to "Create Workflow", then "Import from file". Pick a file from this folder.
2. Read the yellow note called "Read me first".
3. Replace every placeholder that looks like `{{YOUR_EMAIL}}`.
4. Connect your accounts when n8n asks (Gmail, Google Sheets). Never paste passwords into a flow file.
5. Click "Execute workflow" with a test contact (yourself).
6. Only then switch the flow on.

If you get stuck, open `ADAPT-WITH-CLAUDE.md` and paste its prompt to Claude Code.

## F1 Lead Magnet Delivery (`F1-lead-magnet-delivery.json`)
- **What it does:** someone signs up on your form, receives your free booklet, and is saved to your contact sheet with the tag "reader".
- **Flow at a glance:** Form → Clean the fields → Valid email? → Send the booklet → Save contact. (No email → skip.)
- **Connect:** your form (point it at the Webhook), Gmail, a Google Sheet with columns email, firstName, tag, date.
- **Test:** submit your own email. You should get the booklet and see one new row.
- **Success looks like:** the email arrives within a minute, not in spam, one row appears.
- **Common failures:** email lands in spam (check your sending domain setup first); the form sends a different field name (ask Claude to match it).

## F2 Welcome Sequence (`F2-welcome-sequence.json`)
- **What it does:** sends 7 emails over 14 days, each doing one of the six sales.
- **Flow at a glance:** New subscriber → Email 1 → Wait 1 day → Email 2 → Wait 2 days → Email 3 → Wait 2 days → Email 4 → Wait 3 days → Email 5 → Wait 3 days → Email 6 → Wait 3 days → Email 7 (days 0, 1, 3, 5, 8, 11, 14).
- **Connect:** Gmail. Paste your texts from `emails/six-sales-sequence.md`. Start it from F1 or from your email tool.
- **Test:** shorten the waits to one minute, run it for yourself, then restore the waits.
- **Success looks like:** seven emails, in order, with the right name.
- **Common failures:** a buyer keeps getting emails after buying (add a check against your sales sheet); Gmail daily sending limits for big lists (use an email service for volume).

## F3 Sale to Delivery (`F3-sale-to-delivery.json`)
- **What it does:** when your store reports a sale, it sends the files, logs the sale and sends an onboarding email the next day.
- **Flow at a glance:** Sale notification → Pick out the buyer → Send the files → Log the sale → Wait 1 day → Onboarding email.
- **Connect:** your store's sale notification (webhook), Gmail, your sales sheet.
- **Test:** buy your own product once.
- **Success looks like:** files arrive at once; the sheet has the sale.
- **Common failures:** the store sends the same notice twice (ask Claude to ignore repeated order numbers); Amazon KDP does not give you buyer emails, so this is for sales on your own store.

## F4 Pins from Content (`F4-pins-from-content.json`)
- **What it does:** a new chapter or article becomes 5 draft pin texts and image ideas. You approve before anything moves on.
- **Flow at a glance:** New article → AI drafts 5 pins → Ask human → Wait → Approved? → Send to scheduler.
- **Connect:** your AI service (key stored in n8n credentials), Gmail, your pin scheduler.
- **Test:** send a title and summary, approve, check the result; then reject once.
- **Success looks like:** nothing moves until you click Approve.
- **Common failures:** Pinterest shows scheduled pins publicly only after it approves your app; AI text too long for the pin (ask for shorter).

## F5 YouTube Pipeline (`F5-youtube-pipeline.json`)
- **What it does:** idea → script → voice → rendered video → your approval → upload as private.
- **Flow at a glance:** Idea → Script → Voice → Render → Ask human → Wait → Approved? → Upload (private).
- **Connect:** an AI service, a voice service you have rights to use, a render service or script, your YouTube account.
- **Test:** a 10-second video from a three-line script.
- **Success looks like:** a private video in your channel that you watch before publishing.
- **Common failures:** free voice quota ran out (switch tools); render interrupted when the computer sleeps; upload limits.

## F6 Testimonial Request (`F6-testimonial-request.json`)
- **What it does:** 10 days after a purchase it politely asks for feedback, once.
- **Flow at a glance:** Every morning → Read sales sheet → 10+ days and not asked? → Ask → Mark as asked.
- **Connect:** the sales sheet F3 writes, Gmail.
- **Test:** a fake row dated 10 days ago with your email.
- **Success looks like:** one email, the row marked, no repeat tomorrow.
- **Common failures:** wrong date format in the sheet; replies not saved (save good ones by hand and ask permission to quote).

## F7 Weekly Dashboard (`F7-weekly-dashboard.json`)
- **What it does:** every Monday, emails you sales, revenue and subscribers for the last seven days.
- **Flow at a glance:** Monday 7:00 → Read sales → Read subscribers → Add it up → Email me.
- **Connect:** your two sheet tabs, Gmail.
- **Test:** run it by hand on fake rows.
- **Success looks like:** a short email with three numbers.
- **Common failures:** a missing source shows zeros (ask Claude to say "no data" instead).

## F8 Approval Gate (`F8-approval-gate.json`)
- **What it does:** pauses anything public or paid until you click Approve in an email.
- **Flow at a glance:** Request → Email with two links → Wait → Approved? → continue or stop.
- **Connect:** Gmail. Put your address in `{{YOUR_EMAIL}}`.
- **Test:** approve once, reject once.
- **Success looks like:** the flow stays paused until you click.
- **Common failures:** the email goes to spam; the pause link opens on a different n8n address than the one running (set your n8n web address in n8n's settings).
