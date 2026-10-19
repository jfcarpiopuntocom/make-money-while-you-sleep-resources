import fs from 'node:fs';
import {render} from 'pele';
fs.mkdirSync('diagrams',{recursive:true});
const diagrams = {
 '01-business-loop': `flowchart TD\nA[Observe one recurring problem] --> B[Offer a small useful product]\nB --> C[Test with a real buyer]\nC --> D[Improve the product]\nD --> E[Create an honest demonstration]\nE --> F[Buyer chooses and pays]\nF --> G[Store delivers the product]\nG --> H[Support and measure]\nH --> B`,
 '02-multimedia-studio': `flowchart TD\nA[Owned source material] --> B[Product brief]\nB --> C[AI draft or manual draft]\nC --> D[Review facts and usefulness]\nD --> E[Approve exact script and scenes]\nE --> F[Render cards and video locally]\nF --> G[Review picture sound and captions]\nG --> H[Approved asset and destination]\nH --> I[Publish manually]\nG --> J[Revise and render again]\nJ --> D`,
 '03-failure-and-recovery': `flowchart TD\nA[Create unique job ID] --> B[Check saved manifest]\nB --> C{Same job and content}\nC -->|Yes| D[Return existing result]\nC -->|No| E[Reject conflicting reuse]\nB --> F[New job]\nF --> G[Render into temporary folder]\nG --> H{All outputs verified}\nH -->|No| I[Keep failure log and stop]\nH -->|Yes| J[Save hashes and final manifest]\nJ --> D`,
 '04-money-not-magic': `flowchart TD\nA[Customer pays] --> B[Subtract platform and processing fees]\nB --> C[Subtract delivery and support costs]\nC --> D[Subtract customer acquisition]\nD --> E[Contribution per sale]\nE --> F[Recover creation and setup costs]\nF --> G[Account for taxes and other expenses]\nG --> H[Measure actual profit]`
};
// Preserve PELE's font/layout style and bake colors for ebook readers without CSS variables.
const colors={'--pele-bg':'#ffffff','--pele-fg':'#07172d','--pele-muted':'#07172d','--pele-line':'#07172d','--pele-surface':'#ffffff','--pele-surface-alt':'#fff0e8','--pele-border':'#07172d','--pele-accent':'#c43400','--pele-font':'Arial,sans-serif','--_bg':'#ffffff','--_fg':'#07172d','--_m':'#07172d','--_l':'#07172d','--_s':'#ffffff','--_a':'#fff0e8','--_b':'#07172d','--_c':'#c43400','--_r':'4px','--_fm':'monospace'};
for(const [name,source] of Object.entries(diagrams)){
 const out=render(source,{fontSize:21,fontFamily:'Arial',maxWidth:920,padding:28,links:false,images:false});
 if(!out.svg.includes('<svg') || !out.width || !out.height) throw new Error('Invalid SVG');
 let svg=out.svg.replace(/var\((--[\w-]+)(?:,([^()]*))?\)/g,(_,key,fallback)=>colors[key]??fallback??(()=>{throw new Error('Unresolved SVG variable '+key)})());
 svg=svg.replace(/(<svg\b[^>]*>)/,'$1<rect width="100%" height="100%" fill="#ffffff"/>');
 if(svg.includes('var(') || (svg.match(/<svg\b[^>]*>/)?.[0].match(/\sstyle=/g)??[]).length!==1) throw new Error('SVG must have resolved colors and exactly one root style');
 fs.writeFileSync(`diagrams/${name}.mmd`,source+'\n');fs.writeFileSync(`diagrams/${name}.svg`,svg);
 console.log(`${name}: ${out.width} x ${out.height}`);
}
