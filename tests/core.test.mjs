import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {prepareBrief,finishDraft,prepareRender,checkRelease,unitEconomics} from '../lib/core.mjs';
const brief=JSON.parse(fs.readFileSync('examples/brief.json'));
test('Public demo produces an unapproved review package',()=>{
 const b=prepareBrief(brief), d=finishDraft(b,{});
 assert.equal(d.status,'AWAITING_EDITORIAL_REVIEW');assert.equal(d.approved,false);assert.equal(d.scenes.length,3);
 assert.throws(()=>prepareBrief({...brief,source_public:false}));assert.throws(()=>prepareBrief({...brief,job_id:'../../x'}));
});
test('AI response must be structured and useful enough to render',()=>{
 const b=prepareBrief({...brief,mode:'local_ai'});
 assert.throws(()=>finishDraft(b,{message:{content:'not json'}}));
 assert.throws(()=>finishDraft(b,{message:{content:JSON.stringify({headline:'x'})}}));
 const demo=finishDraft(prepareBrief(brief),{});
 assert.equal(finishDraft(b,{message:{content:JSON.stringify(demo)}}).approved,false);
});
test('Render and publication fail closed on missing, changed or expired approval',()=>{
 assert.throws(()=>prepareRender({approved:false}));
 const hash='a'.repeat(64), now=1000;
 const x={manifest:{video_sha256:hash,destination:'my-channel'},approval:{approved:true,asset_sha256:hash,destination:'my-channel',expires_at:new Date(2000).toISOString()}};
 assert.equal(checkRelease(x,now).publishes_automatically,false);
 assert.throws(()=>checkRelease({...x,approval:{...x.approval,asset_sha256:'b'.repeat(64)}},now));
 assert.throws(()=>checkRelease({...x,approval:{...x.approval,destination:'wrong'}},now));
 assert.throws(()=>checkRelease(x,3000));
});
test('Economics distinguishes contribution from profit',()=>{
 const r=unitEconomics({price:20,fee_percent:10,fee_fixed:.5,variable_cost:1,acquisition_cost:4,setup_cost:250});
 assert.equal(r.contribution,12.5);assert.equal(r.break_even_sales,20);
 assert.equal(unitEconomics({price:1,fee_percent:10,fee_fixed:.5,variable_cost:1,acquisition_cost:4,setup_cost:250}).break_even_sales,null);
});
test('All workflow connections resolve and Code nodes parse in the JavaScript sandbox',async()=>{
 const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
 for(const file of fs.readdirSync('workflows')){
  const flow=JSON.parse(fs.readFileSync(`workflows/${file}`));assert.equal(flow.active,false);
  const names=new Set(flow.nodes.map(n=>n.name));
  for(const [name,conn] of Object.entries(flow.connections)){
   assert.ok(names.has(name));for(const output of conn.main)for(const edge of output)assert.ok(names.has(edge.node));
  }
  for(const n of flow.nodes.filter(n=>n.type==='n8n-nodes-base.code'))new AsyncFunction('$input','$',n.parameters.jsCode);
  if(file==='01-product-studio.json'){
   const find=name=>flow.nodes.find(n=>n.name===name).parameters.jsCode;
   let output=await new AsyncFunction('$input','$',find('Edit your brief'))();
   output=await new AsyncFunction('$input','$',find('Prepare AI request'))({all:()=>output});
   const prepared=output[0].json;
   const result=await new AsyncFunction('$input','$',find('Review package'))({first:()=>({json:{}})},()=>({first:()=>({json:prepared})}));
   assert.equal(result[0].json.status,'AWAITING_EDITORIAL_REVIEW');
  }
 }
});
