from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"examples"/"meal-planning-workbook.pdf"
if OUT.exists():raise SystemExit("Preserve existing workbook")
W,H=612,792
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle("Meal Planning Example Workbook");c.setAuthor("J. F. Carpio")
NAVY=colors.HexColor("#081A30")
def text(x,y,t,size=11,bold=False):
 c.setFillColor(NAVY);c.setFont("Helvetica-Bold" if bold else "Helvetica",size);c.drawString(x,y,t)
def header(title,filled,page):
 text(44,748,"MEAL PLANNING EXAMPLE",10,True);text(44,712,title,24,True)
 text(44,687,"Completed teaching example" if filled else "Your worksheet — type in the fields or print",11)
 text(44,665,"Adapt the plan to your household, preferences and existing supplies.",10)
 c.setStrokeColor(NAVY);c.line(44,650,568,650)
 text(44,32,"Companion example • Make Money While You Sleep • J. F. Carpio",9)
 text(545,32,str(page),9)
def field(name,x,y,w,h,value="",multi=False):
 c.acroForm.textfield(name=name,tooltip=name.replace("_"," "),x=x,y=y,width=w,height=h,value=value,
  borderWidth=1,borderStyle="solid",borderColor=NAVY,fillColor=colors.white,textColor=colors.black,
  fontName="Helvetica",fontSize=11,forceBorder=True,fieldFlags="multiline" if multi else "")
page=0
for filled in [False,True]:
 tag="example" if filled else "blank"
 page+=1;header("1. Check what you have",filled,page)
 text(44,620,"Item",11,True);text(300,620,"Amount / use first",11,True)
 pantry=[("Rice","One bag"),("Lentils","Half a bag"),("Frozen vegetables","One bag"),("Eggs","Four"),("Pasta","One packet"),("Tinned tomatoes","Two tins")]
 for i,(item,amount) in enumerate(pantry):
  y=572-i*50;field(f"{tag}_pantry_item_{i}",44,y,240,34,item if filled else "");field(f"{tag}_pantry_amount_{i}",300,y,268,34,amount if filled else "")
 text(44,252,"What should we use first?",11,True)
 field(f"{tag}_use_first",44,143,524,90,"Use eggs and any fresh ingredients already in the fridge." if filled else "",True)
 text(44,112,"Check storage and food safety guidance that applies to the ingredients you use.",10)
 c.showPage()
 page+=1;header("2. Choose the week",filled,page)
 text(44,620,"Day",11,True);text(150,620,"Meal / plan",11,True)
 days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
 meals=["Rice, lentils and vegetables","Pasta with tomato sauce","Eggs with vegetables and toast","Flexible evening: reuse what is left","Bean wraps","Repeat a household favourite","Review supplies and plan the next shop"]
 for i,(day,meal) in enumerate(zip(days,meals)):
  y=564-i*53;text(44,y+12,day);field(f"{tag}_meal_{i}",150,y,418,37,meal if filled else "")
 text(44,154,"Keep one evening flexible. Change the plan when the week changes.",11)
 c.showPage()
 page+=1;header("3. Write one shopping list",filled,page)
 groups=[("Fresh items","Wrap fillings and any fresh ingredients missing from the plan"),
 ("Cupboard items","Beans and wraps if not already available"),
 ("Other items","Bread if needed; check the pantry before adding more"),
 ("Before paying","Remove duplicates. Check quantities against the meals and existing supplies.")]
 for i,(label,val) in enumerate(groups):
  y=612-i*120;text(44,y,label,12,True);field(f"{tag}_shopping_{i}",44,y-92,524,77,val if filled else "",True)
 text(44,96,"This is an illustration of a planning process, not nutrition or medical advice.",10)
 c.showPage()
c.save()
print(json.dumps({"workbook":str(OUT),"bytes":OUT.stat().st_size,"sha256":hashlib.sha256(OUT.read_bytes()).hexdigest()}))

