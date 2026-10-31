from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/pdf/ArthiX_Overview.pdf'; OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=960,540
NAVY='#10172A'; NAVY2='#17223C'; INK='#18233B'; MUTED='#66728A'; BLUE='#5B7CFA'; CYAN='#48D5CE'; PURPLE='#9B8CFF'; PAPER='#F6F8FC'; WHITE='#FFFFFF'; LINE='#E4E9F2'; PALE='#E9EEFF'; MINT='#E1F8F4'; GOLD='#FFC86B'; DARKM='#B5C2DC'
pdfmetrics.registerFont(TTFont('Segoe','C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('Segoe-Bold','C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFont(TTFont('Segoe-Italic','C:/Windows/Fonts/segoeuii.ttf'))
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('ArthiX | Product overview'); c.setAuthor('ArthiX')

def rect(x,y,w,h,fill,r=14,stroke=None,sw=1):
    c.setFillColor(HexColor(fill))
    if stroke: c.setStrokeColor(HexColor(stroke)); c.setLineWidth(sw)
    else: c.setStrokeColor(HexColor(fill))
    c.roundRect(x,y,w,h,r,fill=1,stroke=1 if stroke else 0)
def txt(x,y,s,size=12,color=INK,bold=False,font=None):
    c.setFillColor(HexColor(color)); c.setFont(font or ('Segoe-Bold' if bold else 'Segoe'),size); c.drawString(x,y,s)
def right(x,y,s,size=12,color=INK,bold=False):
    c.setFillColor(HexColor(color)); c.setFont('Segoe-Bold' if bold else 'Segoe',size); c.drawRightString(x,y,s)
def para(x,y,s,width,size=12,color=INK,leading=None,bold=False,maxlines=99):
    font='Segoe-Bold' if bold else 'Segoe'; leading=leading or size*1.42
    lines=simpleSplit(s,font,size,width)[:maxlines]
    c.setFillColor(HexColor(color)); c.setFont(font,size)
    for i,line in enumerate(lines): c.drawString(x,y-i*leading,line)
    return y-len(lines)*leading
def circle(x,y,r,fill,stroke=None):
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke or fill)); c.circle(x,y,r,fill=1,stroke=1 if stroke else 0)
def base(n,section,dark=False):
    bg=NAVY if dark else PAPER
    c.setFillColor(HexColor(bg)); c.rect(0,0,W,H,fill=1,stroke=0)
    if dark:
        # subtle brand glows
        circle(900,490,160,'#182443'); circle(930,485,90,'#1C2B4B')
    else:
        c.setStrokeColor(HexColor('#E8EDF5')); c.setLineWidth(.5)
        for x in range(40,960,32): c.line(x,0,x,H)
        for y in range(20,540,32): c.line(0,y,W,y)
        c.setFillColor(HexColor(PAPER)); c.setFillAlpha(.88); c.rect(0,0,W,H,fill=1,stroke=0); c.setFillAlpha(1)
    color=DARKM if dark else MUTED
    txt(44,505,'ARTHIX',10,CYAN if dark else BLUE,True)
    txt(112,505,section.upper(),8,color,True)
    right(916,505,f'{n:02d}  /  10',9,color)
    c.setStrokeColor(HexColor('#2A3550' if dark else LINE)); c.setLineWidth(.8); c.line(44,32,916,32)
    txt(44,17,'ONE WORKSPACE FOR THE WORK BEHIND YOUR BUSINESS',7,color,True)
    right(916,17,'ARTHIX  •  PRODUCT OVERVIEW',7,color)
def title(kicker,headline,sub=None,dark=False,y=450):
    col=CYAN if dark else BLUE; main=WHITE if dark else INK; muted=DARKM if dark else MUTED
    txt(50,y,kicker.upper(),9,col,True)
    txt(50,y-42,headline,30,main,True)
    if sub: para(51,y-68,sub,600,12,muted,17)
def pill(x,y,label,bg=PALE,fg=BLUE,w=None):
    w=w or pdfmetrics.stringWidth(label,'Segoe-Bold',9)+25
    rect(x,y,w,24,bg,12); txt(x+12,y+8,label,9,fg,True)
def card(x,y,w,h,heading,body,accent=BLUE,dark=False):
    bg=NAVY2 if dark else WHITE; main=WHITE if dark else INK; muted=DARKM if dark else MUTED
    rect(x,y,w,h,bg,16,stroke='#273553' if dark else LINE)
    rect(x+16,y+h-22,24,4,accent,2)
    txt(x+16,y+h-49,heading,14,main,True)
    para(x+16,y+h-69,body,w-32,10,muted,14)
def icon_box(x,y,label,sub,color=BLUE):
    rect(x,y,188,83,WHITE,15,stroke=LINE)
    circle(x+27,y+53,12,color); txt(x+23,y+49,'+',11,WHITE,True)
    txt(x+48,y+52,label,12,INK,True); txt(x+48,y+32,sub,9,MUTED)

# 1 — cover
base(1,'INTRODUCTION',True)
txt(58,420,'THE BUSINESS,',12,CYAN,True); txt(58,365,'in one',52,WHITE,True); txt(58,304,'clear workspace.',46,WHITE,True)
para(61,262,'A practical, self-hosted business platform for the work behind your company.',400,16,DARKM,23)
pill(62,173,'OPEN SOURCE  ·  MODULAR  ·  SELF-HOSTED','#243352',WHITE,225)
# floating UI card
rect(548,119,347,304,'#F7F9FD',20)
rect(548,367,347,56,WHITE,20); c.setFillColor(HexColor(WHITE)); c.rect(548,367,347,20,fill=1,stroke=0)
txt(570,390,'ArthiX',17,INK,True); txt(828,391,'●  Overview',9,MUTED)
rect(570,313,302,39,'#EDF1FF',10); txt(584,336,'Good morning',9,BLUE,True); txt(584,321,'Your business, in focus',14,INK,True)
for i,(lab,val) in enumerate([('CUSTOMERS','248'),('OPEN ITEMS','12'),('MONTH TO DATE','$18.4k')]):
    x=570+i*103; rect(x,249,94,52,WHITE,9,stroke=LINE); txt(x+9,280,lab,6,MUTED,True); txt(x+9,260,val,14,INK,True)
txt(570,225,'Activity at a glance',10,INK,True)
for i,h in enumerate([25,41,33,59,50,73,65,91,78]):
    rect(578+i*30,152,15,h,[BLUE,'#879CFC','#AEBBFB'][i%3],6)
txt(570,136,'CRM     FINANCE     PEOPLE     OPERATIONS',7,MUTED,True)
circle(875,430,7,CYAN); c.showPage()

# 2 — why
base(2,'THE OPPORTUNITY')
title('THE EVERYDAY CHALLENGE','Business work gets scattered','People lose time switching tools, repeating updates, and hunting for the latest context.')
# messy inputs -> shared workspace
labels=[('CUSTOMERS','Chats, contacts, follow-ups'),('MONEY','Invoices, expenses, approvals'),('PEOPLE','Schedules, projects, records'),('OPERATIONS','Stock, vendors, service')]
for i,(a,b) in enumerate(labels):
    x=54+(i%2)*224; y=283-(i//2)*112
    rect(x,y,204,87,WHITE,15,stroke=LINE); circle(x+24,y+58,9,[BLUE,CYAN,PURPLE,GOLD][i]); txt(x+43,y+60,a,9,MUTED,True); txt(x+18,y+29,b,11,INK,True)
    if i in (0,1):
        c.setStrokeColor(HexColor('#BCC6DA')); c.setDash(3,3); c.line(x+204,y+44,550,y+44); c.setDash()
rect(557,220,337,160,NAVY,21)
circle(597,330,16,CYAN); txt(589,326,'A',12,NAVY,True)
txt(627,334,'ONE SHARED WORKSPACE',9,CYAN,True); txt(580,291,'See the context.',22,WHITE,True); txt(580,258,'Find the next step.',22,WHITE,True)
para(580,235,'Related work stays connected, visible, and easier to act on.',285,10,DARKM,14)
pill(558,157,'LESS FRAGMENTATION  →  MORE CLARITY',MINT,'#19877F',300)
c.showPage()

# 3 — platform
base(3,'THE PLATFORM')
title('ONE PLATFORM, CONNECTED AREAS','The tools your team returns to','Move between customer work, money, people, and operations without losing the bigger picture.')
modules=[('CRM','Companies, contacts, deals'),('FINANCE','Invoices, expenses, budgets'),('PEOPLE','HR, payroll, schedules'),('PROJECTS','Tasks and delivery'),('SERVICE','Support desk and knowledge'),('INVENTORY','Products and stock'),('VENDORS','Purchasing and suppliers'),('WORKFLOWS','Rules and automation')]
for i,(a,b) in enumerate(modules):
    col=i%4; row=i//4; x=50+col*220; y=275-row*112
    rect(x,y,204,88,WHITE,15,stroke=LINE)
    circle(x+25,y+59,11,[BLUE,CYAN,PURPLE,GOLD][col]); txt(x+22,y+56,str(i+1),8,WHITE,True)
    txt(x+45,y+62,a,10,INK,True); para(x+17,y+34,b,170,9,MUTED,12)
rect(51,61,858,51,'#E9EEFF',14); txt(70,91,'ONE SET OF SHARED RECORDS',9,BLUE,True)
txt(70,73,'Connected context helps teams follow work from the first request to the next action.',11,INK)
c.showPage()

# 4 — dashboard
base(4,'A CLEAR STARTING POINT',True)
title('SEE WHAT NEEDS ATTENTION','A dashboard built for momentum','Start with a high-level view, then open the records behind each item.',True)
c.saveState(); c.translate(0,-62)
rect(513,100,376,327,'#F8FAFE',18)
txt(537,395,'Business overview',15,INK,True); txt(537,375,'Welcome back. Here’s the latest.',9,MUTED)
for i,(lab,val,delta) in enumerate([('OPEN DEALS','18','+ 4 this week'),('INVOICES DUE','06','Needs review'),('TEAM REQUESTS','12','3 pending')]):
    x=533+i*112; rect(x,296,101,62,WHITE,10,stroke=LINE); txt(x+10,340,lab,6,MUTED,True); txt(x+10,318,val,21,INK,True); txt(x+10,304,delta,7,BLUE)
txt(537,271,'Recent activity',10,INK,True)
for i,(tag,desc) in enumerate([('CRM','New company added'),('FINANCE','Expense submitted'),('PEOPLE','Leave request updated')]):
    y=235-i*48; circle(546,y+4,7,[BLUE,CYAN,PURPLE][i]); txt(562,y+9,tag,7,BLUE,True); txt(562,y-7,desc,9,INK); right(863,y,'TODAY',7,MUTED)
rect(532,121,338,7,'#E7EBF3',4)
for i,h in enumerate([25,45,36,61,49,75,64]): rect(554+i*40,140,20,h,[BLUE,'#8C9DF8'][i%2],6)
c.restoreState()
card(56,205,198,123,'ONE VIEW','Key activity starts in one place.',CYAN,True)
card(270,205,198,123,'USEFUL DETAIL','Follow a number to its source record.',BLUE,True)
card(56,70,412,117,'A SIMPLE RHYTHM','Review what changed. Open the detail. Take the next step.',PURPLE,True)
c.showPage()

# 5 — CRM
base(5,'CUSTOMER RELATIONSHIPS')
title('CRM','Know the people behind the work','Keep company and contact records, opportunities, and activity together.')
stages=[('NEW','Meet'),('QUALIFIED','Understand'),('IN PROGRESS','Work together'),('WON','Keep growing')]
for i,(a,b) in enumerate(stages):
    x=53+i*217; rect(x,271,190,88,WHITE,14,stroke=LINE); rect(x+14,330,69,18,[PALE,MINT,'#EEEAFE','#FFF2D7'][i],9); txt(x+22,336,a,7,[BLUE,'#19877F',PURPLE,'#9B6B00'][i],True); txt(x+14,298,b,13,INK,True)
    if i<3: txt(x+194,364,'›',22,BLUE,True)
txt(55,236,'A RELATIONSHIP, WITH CONTEXT',9,BLUE,True)
cards=[('01','Capture','Create a company or contact record.'),('02','Connect','Link conversations, deals, and details.'),('03','Continue','See the history and decide what comes next.')]
for i,(n,a,b) in enumerate(cards):
    x=53+i*288; rect(x,102,263,108,WHITE,16,stroke=LINE); txt(x+17,177,n,10,CYAN,True); txt(x+55,177,a,15,INK,True); para(x+17,147,b,225,10,MUTED,14)
rect(54,51,851,32,NAVY,12); txt(73,63,'A shared customer view helps a small team stay coordinated as relationships grow.',10,WHITE)
c.showPage()

# 6 — operations
base(6,'DAILY OPERATIONS',True)
title('FROM REQUEST TO RESOLUTION','Keep everyday work moving','Focused work areas help teams handle the details and keep decisions visible.',True)
ops=[('MONEY','Invoices · Expenses · Budgets'),('PEOPLE','Team · Payroll · Time'),('SERVICE','Requests · Support · Knowledge'),('OPERATIONS','Inventory · Vendors · Purchasing')]
for i,(a,b) in enumerate(ops):
    x=54+(i%2)*225; y=280-(i//2)*120; accent=[CYAN,BLUE,PURPLE,GOLD][i]
    rect(x,y,204,94,NAVY2,15,stroke='#2A3550'); circle(x+25,y+64,11,accent); txt(x+22,y+61,'+',10,NAVY,True); txt(x+47,y+66,a,9,accent,True); para(x+17,y+38,b,168,10,WHITE,14)
rect(540,175,347,174,'#202D4B',19)
txt(565,315,'A CLEAR APPROVAL PATH',9,CYAN,True)
steps=[('Request',570,252),('Review',681,252),('Decision',792,252)]
for i,(s,x,y) in enumerate(steps):
    circle(x,y,26,BLUE if i==1 else '#354467'); txt(x-21,y-4,s,9,WHITE,True)
    if i<2: c.setStrokeColor(HexColor(CYAN)); c.setLineWidth(2); c.line(x+29,y,x+77,y)
para(565,207,'Requests and approvals give important work a visible next step.',285,11,DARKM,16)
pill(541,126,'FINANCE  ·  PEOPLE  ·  SERVICE  ·  OPERATIONS','#293653',WHITE,310)
c.showPage()

# 7 — AI and automation
base(7,'SMARTER ROUTINES')
title('AUTOMATION + OPTIONAL AI','Spend less time on repeat steps','Use workflows for routine actions. Add AI assistance where it helps your team.')
rect(54,121,518,224,WHITE,18,stroke=LINE)
txt(78,314,'A SIMPLE WORKFLOW',9,BLUE,True)
nodes=[('WHEN','A record changes'),('CHECK','A rule matches'),('THEN','Take an action')]
for i,(a,b) in enumerate(nodes):
    x=78+i*164; rect(x,209,139,73,[PALE,MINT,'#EEEAFE'][i],12); txt(x+13,259,a,8,[BLUE,'#19877F',PURPLE][i],True); para(x+13,237,b,115,11,INK,14,True)
    if i<2: txt(x+141,236,'→',18,BLUE,True)
para(79,172,'Examples: send a notification, update a field, create a record, or call a webhook.',438,10,MUTED,14)
rect(602,121,304,224,NAVY,18)
circle(638,296,13,CYAN); txt(633,292,'✦',11,NAVY,True)
txt(663,301,'AI, when configured',14,WHITE,True)
para(625,261,'Draft, summarize, and suggest next actions with an AI provider connected to your setup.',250,11,DARKM,16)
rect(625,159,256,50,'#253351',12); txt(642,188,'Human review stays in the loop.',10,CYAN,True); txt(642,170,'Configure the provider for AI features.',8,DARKM)
pill(55,65,'AI FEATURES REQUIRE A CONFIGURED PROVIDER',PALE,BLUE,322)
c.showPage()

# 8 — demo
base(8,'A SAMPLE BUSINESS')
title('MEET STRIDEWORKS FOOTWEAR','A demo company you can explore','Illustrative sample data shows how customer, product, and business work can connect.')
# retail illustration shelves / shoes
rect(54,105,352,249,NAVY,19)
txt(79,320,'STRIDEWORKS',11,CYAN,True); txt(79,293,'Move well.',27,WHITE,True); txt(79,261,'Everyday footwear, thoughtfully made.',10,DARKM)
rect(80,154,300,12,'#2B3957',6)
for i,(col,x) in enumerate([(BLUE,99),(CYAN,181),(PURPLE,263)]):
    circle(x+24,209,24,col); rect(x,187,49,18,WHITE,7); txt(x+3,163,['RUN','WALK','WORK'][i],7,DARKM,True)
flow=[('CUSTOMERS','People and relationships'),('PRODUCTS','Catalog and stock'),('SALES','Orders and follow-ups'),('OPERATIONS','Vendors and delivery')]
for i,(a,b) in enumerate(flow):
    x=453+(i%2)*223; y=244-(i//2)*111
    rect(x,y,202,86,WHITE,14,stroke=LINE); txt(x+15,y+59,a,8,[BLUE,CYAN,PURPLE,'#B07A17'][i],True); txt(x+15,y+35,b,11,INK,True)
rect(454,76,425,34,MINT,12); txt(470,89,'DEMO DATA ONLY  ·  NOT REAL CUSTOMER RECORDS',8,'#19877F',True)
c.showPage()

# 9 — architecture
base(9,'BUILT TO RUN YOUR WAY',True)
title('SELF-HOSTED BY DESIGN','Your deployment. Your operating choices.','A modular web application with an API, relational database, and supporting services.',True)
layers=[('ADMIN WEB','Next.js interface','The team’s workspace'),('API','Node.js · Hono','Business endpoints'),('DATA','PostgreSQL · Redis','Records and supporting services')]
for i,(a,b,d) in enumerate(layers):
    x=54+i*286; rect(x,238,253,133,NAVY2,17,stroke='#31405F'); txt(x+20,338,a,9,[CYAN,BLUE,PURPLE][i],True); txt(x+20,304,b,16,WHITE,True); txt(x+20,278,d,9,DARKM)
    if i<2: txt(x+261,292,'→',22,CYAN,True)
rect(54,138,825,55,'#202D4B',14); txt(74,168,'SELF-HOSTED',9,CYAN,True); txt(74,149,'Deploy on infrastructure you operate; configure secrets, backups, and integrations for your environment.',10,WHITE)
para(55,105,'AI capabilities and external integrations depend on provider credentials and the deployed configuration. Feature availability may vary by version.',820,9,DARKM,13)
c.showPage()

# 10 — getting started
base(10,'GET STARTED')
title('START SMALL. MAKE IT YOURS.','Bring your business into focus.','A simple path from first launch to a workspace shaped around your team.')
journey=[('01','RUN','Start the stack with the project’s Docker Compose setup.'),('02','EXPLORE','Open the admin app and navigate the key work areas.'),('03','LOAD DEMO','Use the StrideWorks sample to explore connected records.'),('04','CONFIGURE','Set real secrets, integrations, AI provider, and backups.')]
for i,(n,a,b) in enumerate(journey):
    x=54+i*216; circle(x+18,323,17,BLUE if i<3 else CYAN); txt(x+8,319,n,8,WHITE,True); txt(x,282,a,10,BLUE if i<3 else '#19877F',True); para(x,257,b,177,10,MUTED,14)
    if i<3: c.setStrokeColor(HexColor('#C8D1E3')); c.setLineWidth(1.5); c.line(x+41,323,x+198,323)
rect(54,104,851,83,NAVY,18)
txt(79,157,'ARTHIX',9,CYAN,True); txt(79,129,'One workspace for the work behind your business.',20,WHITE,True)
right(877,143,'Explore. Connect. Grow.',10,DARKM,True)
para(55,75,'For exact setup commands and configuration, follow the current repository README and environment example. Change demo credentials before exposing the deployment.',830,9,MUTED,13)
c.showPage(); c.save()
print(f'Created {OUT} (10 slides, 16:9 landscape)')
