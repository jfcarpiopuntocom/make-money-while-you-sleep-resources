import fs from 'node:fs';
import {prepareBrief, finishDraft, prepareRender, checkRelease, unitEconomics} from '../lib/core.mjs';
fs.mkdirSync('workflows', {recursive: true});
const node = (name, type, parameters, x, y=200, extra={}) => ({id: name.replaceAll(' ', '-'), name, type: `n8n-nodes-base.${type}`, typeVersion: type === 'code' ? 2 : type === 'httpRequest' ? 4.2 : type === 'if' ? 2.2 : 1, position: [x,y], parameters, ...extra});
const code = (fn, expression) => ({jsCode: `${fn.toString()}\n${expression}`});
const trigger = node('Start manually', 'manualTrigger', {}, 0);
const sample = {job_id:'meal-plan-demo', mode:'demo', source_public:true, product:'Weekly Meal Planning Kit', audience:'busy households planning meals', problem:'deciding what to cook before shopping', model:'qwen2.5:7b', source_text:'The kit contains a weekly meal worksheet, a pantry check, a shopping list and a flexible evening. Start with meals the household already knows. Check ingredients already available. Plan meals, list missing ingredients and quantities, and leave one evening flexible. No nutrition or savings claim is made.'};
const demo = node('Edit your brief', 'code', {jsCode:`return [{json:${JSON.stringify(sample)}}];`},200);
const prep = node('Prepare AI request', 'code', code(prepareBrief,'return $input.all().map(i => ({json:prepareBrief(i.json)}));'),400);
const branch = node('Demo mode', 'if', {conditions:{options:{caseSensitive:true,leftValue:'',typeValidation:'strict',version:2},conditions:[{id:'demo-check',leftValue:'={{ $json.mode }}',rightValue:'demo',operator:{type:'string',operation:'equals'}}],combinator:'and'},options:{}},600);
const noCost = node('Demo response', 'code', {jsCode:'return [{json:{demo:true}}];'},800,100);
const ai = node('Local Ollama', 'httpRequest', {method:'POST',url:'http://localhost:11434/api/chat',sendBody:true,specifyBody:'json',jsonBody:'={{ JSON.stringify({model:$json.model,stream:false,format:"json",messages:[{role:"user",content:$json.prompt}]}) }}',options:{timeout:120000}},800,350);
const finish = node('Review package', 'code', code(finishDraft,'const brief = $("Prepare AI request").first().json; return [{json:finishDraft(brief,$input.first().json)}];'),1050);
function save(name,nodes,connections){fs.writeFileSync(`workflows/${name}.json`,JSON.stringify({name,active:false,nodes,connections,settings:{executionOrder:'v1'},pinData:{}},null,2));}
const edge = name => ({node:name,type:'main',index:0});
save('01-product-studio',[trigger,demo,prep,branch,noCost,ai,finish],{
 'Start manually':{main:[[edge('Edit your brief')]]},'Edit your brief':{main:[[edge('Prepare AI request')]]},'Prepare AI request':{main:[[edge('Demo mode')]]},'Demo mode':{main:[[edge('Demo response')],[edge('Local Ollama')]]},'Demo response':{main:[[edge('Review package')]]},'Local Ollama':{main:[[edge('Review package')]]}
});
const renderInput = node('Approved render input','code',{jsCode:'throw new Error("Paste your reviewed package here; set approved:true and the exact script_sha256. See docs/QUICKSTART.md.");'},200);
const renderPrep = node('Validate render approval','code',code(prepareRender,'return $input.all().map(i => ({json:prepareRender(i.json)}));'),400);
const render = node('Local media studio','httpRequest',{method:'POST',url:'http://127.0.0.1:8765/render',authentication:'genericCredentialType',genericAuthType:'httpHeaderAuth',sendBody:true,specifyBody:'json',jsonBody:'={{ JSON.stringify($json) }}',options:{timeout:120000}},650);
const review = node('Inspect local result','code',{jsCode:'const r=$input.first().json; if(r.status!=="READY_FOR_REVIEW" || !r.video_sha256 || !r.output_dir) throw new Error("Render not complete: inspect local logs and do not publish."); return [{json:{...r,approved:false,next_action:"Open the local video and manifest, then review."}}];'},900);
save('02-local-multimedia-studio',[trigger,renderInput,renderPrep,render,review],{'Start manually':{main:[[edge('Approved render input')]]},'Approved render input':{main:[[edge('Validate render approval')]]},'Validate render approval':{main:[[edge('Local media studio')]]},'Local media studio':{main:[[edge('Inspect local result')]]}});
const approval = node('Exact approval input','code',{jsCode:'return [{json:{manifest:{video_sha256:"",destination:""},approval:{approved:false,asset_sha256:"",destination:"",expires_at:""}}}];'},200);
const gate = node('Check exact asset and destination','code',code(checkRelease,'return $input.all().map(i => ({json:checkRelease(i.json)}));'),450);
save('03-publication-review',[trigger,approval,gate],{'Start manually':{main:[[edge('Exact approval input')]]},'Exact approval input':{main:[[edge('Check exact asset and destination')]]}});
const moneyInput = node('Edit assumptions','code',{jsCode:'return [{json:{price:20,fee_percent:10,fee_fixed:0.5,variable_cost:1,acquisition_cost:4,setup_cost:250}}];'},200);
const money = node('Contribution and break even','code',code(unitEconomics,'return $input.all().map(i => ({json:unitEconomics(i.json)}));'),450);
save('04-unit-economics',[trigger,moneyInput,money],{'Start manually':{main:[[edge('Edit assumptions')]]},'Edit assumptions':{main:[[edge('Contribution and break even')]]}});
fs.mkdirSync('examples',{recursive:true});fs.writeFileSync('examples/brief.json',JSON.stringify(sample,null,2));
console.log('Wrote inactive workflows and demo brief; no n8n instance was changed.');
