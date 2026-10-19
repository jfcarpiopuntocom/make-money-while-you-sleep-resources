import fs from 'node:fs';
import crypto from 'node:crypto';
import {prepareBrief, finishDraft} from '../lib/core.mjs';
const brief=JSON.parse(fs.readFileSync('examples/brief.json','utf8'));
const d=finishDraft(prepareBrief(brief),{});
fs.writeFileSync('examples/review-package.json',JSON.stringify(d,null,2));
const job={job_id:'meal-plan-demo-video',title:d.product,approved:true,script_text:d.script,script_sha256:crypto.createHash('sha256').update(d.script).digest('hex'),scenes:d.scenes,seconds_per_scene:3};
// This is an explicitly owned synthetic example, not approval of reader content.
fs.writeFileSync('examples/approved-demo-render.json',JSON.stringify(job,null,2));
fs.writeFileSync('examples/unit-economics.csv','assumption,illustrative_value\nprice,20\nfee_percent,10\nfee_fixed,0.50\nvariable_cost,1\nacquisition_cost,4\nsetup_cost,250\ncontribution_before_tax,12.50\nbreak_even_sales,20\n');
console.log('Created a synthetic review package and local render example.');
