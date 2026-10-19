"""Create a readable entry point from the supplied example, without requiring code."""
from pathlib import Path
import json
from html import escape

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
import pypdfium2 as pdfium

root=Path(__file__).resolve().parents[1]
out=root/'examples'/'START-HERE.pdf'
assert not out.exists(), 'Keep the existing reader entry point.'
brief=json.loads((root/'examples'/'brief.json').read_text('utf8'))
sample=json.loads((root/'examples'/'review-package.json').read_text('utf8'))
navy=HexColor('#001526')
body=ParagraphStyle('body',fontName='Helvetica',fontSize=10.6,leading=15,textColor=navy,spaceAfter=10)
h1=ParagraphStyle('heading',parent=body,fontName='Helvetica-Bold',fontSize=23,leading=27,spaceAfter=18)
h2=ParagraphStyle('subheading',parent=body,fontName='Helvetica-Bold',fontSize=13,leading=17,spaceBefore=8,spaceAfter=8)
story=[]
def p(text):story.append(Paragraph(text,body))
def heading(text):story.append(Paragraph(text,h2))
story.append(Paragraph('Start here',h1))
p('<b>Make Money While You Sleep (Using AI and Automations)</b><br/>Reader resources · J. F. Carpio')
p('Use this <b>completed teaching example</b> before adapting the process to your own topic. It is not a record of achieved sales or income.')
heading('Open the workbook')
p('Open <b>meal-planning-workbook.pdf</b> in this same examples folder. Its first pages are blank worksheets; the later pages show a completed example. Type into the fields and save a copy, or print them.')
p('Work through the <b>pantry check, weekly plan and shopping list</b>. Leave room for the evening when plans change. The example makes no nutrition, health or savings promise.')
heading('Read the product brief')
p('<b>Product:</b> '+escape(brief['product']))
p('<b>Audience:</b> '+escape(brief['audience'])+'<br/><b>Problem:</b> '+escape(brief['problem']))
p('<b>Source:</b> '+escape(brief['source_text']))
p('The <b>source is the reference</b> for the demonstration. Check that every instruction agrees with the worksheet. You can complete this route in your normal writing and design tools; no n8n, AI account or programming is required.')
story.append(PageBreak())
story.append(Paragraph('See the demonstration',h1))
heading('Short article')
p(escape(sample['article']))
heading('Spoken script')
p(escape(sample['script']))
heading('Three scenes')
for i,scene in enumerate(sample['scenes'],1):
    p('<b>'+str(i)+'. '+escape(scene['title'])+'</b><br/>'+escape(scene['body']))
heading('Caption')
p(escape(sample['caption']))
p('<b>Review before sharing:</b> Does the demonstration match the workbook? Can someone use the instructions without buying something else? The supplied video example is silent; review any narration and captions you add yourself.')
story.append(PageBreak())
story.append(Paragraph('Build your own example',h1))
p('Choose a <b>problem you understand</b>. Write who needs help, when they need it, and what they should be able to finish after using your product.')
p('Use <b>templates/product-brief.md</b> and <b>templates/review-checklist.md</b> as writing prompts. A normal text editor can open them. You can also copy their questions into your preferred writing tool.')
p('Make a <b>completed example and a blank worksheet</b>. Ask someone in the intended audience to follow the instructions without your explanation. Revise the step where they get stuck.')
heading('Check the money')
p('The example in <b>unit-economics.csv</b> assumes a $20 price, a 10% fee plus $0.50, $1 of variable costs and $4 to acquire a buyer. That leaves <b>$12.50 contribution</b> before taxes and other omitted costs. With $250 in setup costs, twenty sales at that contribution recover setup.')
p('These are <b>illustrative assumptions</b>, not a quotation from a platform or a sales forecast. Use your actual fees and records. A spreadsheet can open the CSV, or you can do the calculation on paper.')
heading('Keep control of your work')
p('Keep a <b>saved copy</b> of your source, finished product and demonstration. Use the diagrams in diagrams/ to inspect the process. Open <b>ADAPT-WITH-YOUR-AI.md</b> in the main folder for a copyable prompt: your AI can adapt the starting designs to your own product and tools. Read docs/QUICKSTART.md for the supplied technical design; verify your adapted version before using it.')
p('A <b>complete first transaction</b> means a buyer understands the offer, receives the promised files and can use them. Review checkout and delivery through your chosen platform\'s permitted test route before accepting orders.')

def footer(c,doc):
    c.setFont('Helvetica',8);c.setFillColor(navy)
    c.drawString(36,20,'Practical Business Guides · JFCarpio.com')
    c.drawRightString(396,20,str(doc.page))
SimpleDocTemplate(str(out),pagesize=(432,648),leftMargin=36,rightMargin=36,topMargin=36,bottomMargin=36,title='Reader resources Start here',author='J. F. Carpio').build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(out)
assert len(reader.pages)==3,len(reader.pages)
text='\n'.join(page.extract_text() for page in reader.pages)
assert '$12.50' in text and sample['scenes'][0]['title'] in text
qa=root.parent/'001-launch-review'/'reader-start-review'
qa.mkdir(exist_ok=True)
pdf=pdfium.PdfDocument(out)
for i in range(len(pdf)):
    pdf[i].render(scale=2).to_pil().save(qa/f'page-{i+1}.png')
print('Created readable start PDF; workbook, example and calculation included. No workflow executed.')
