from pathlib import Path
import math, subprocess, asyncio, textwrap, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import edge_tts

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; PDF=OUT/'pdf'/'ArthiX_Overview.pdf'; VIDEO=OUT/'video'/'ArthiX_Product_Introduction.mp4'
TMP=ROOT/'tmp'/'arthix_media'; TMP.mkdir(parents=True,exist_ok=True); PDF.parent.mkdir(parents=True,exist_ok=True); VIDEO.parent.mkdir(parents=True,exist_ok=True)
NAVY='#10172A'; INK='#18233B'; MUTED='#63708B'; BLUE='#5B7CFA'; CYAN='#48D5CE'; PALE='#F4F7FC'; WHITE='#FFFFFF'; LILAC='#A599FF'

# PDF
fontdir=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Segoe','segoeui.ttf')); pdfmetrics.registerFont(TTFont('Segoe-Bold','segoeuib.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Hero',fontName='Segoe-Bold',fontSize=32,leading=38,textColor=colors.HexColor(NAVY),spaceAfter=13))
styles.add(ParagraphStyle(name='Deck',fontName='Segoe',fontSize=13,leading=19,textColor=colors.HexColor(MUTED),spaceAfter=15))
styles.add(ParagraphStyle(name='H2x',fontName='Segoe-Bold',fontSize=20,leading=25,textColor=colors.HexColor(NAVY),spaceBefore=5,spaceAfter=10))
styles.add(ParagraphStyle(name='H3x',fontName='Segoe-Bold',fontSize=11,leading=15,textColor=colors.HexColor(INK),spaceBefore=7,spaceAfter=3))
styles.add(ParagraphStyle(name='Bodyx',fontName='Segoe',fontSize=9.3,leading=14,textColor=colors.HexColor(INK),spaceAfter=6))
styles.add(ParagraphStyle(name='Smallx',fontName='Segoe',fontSize=8,leading=11,textColor=colors.HexColor(MUTED)))
styles.add(ParagraphStyle(name='Quote',fontName='Segoe-Bold',fontSize=15,leading=21,textColor=colors.HexColor(BLUE),leftIndent=14,rightIndent=14,spaceBefore=8,spaceAfter=10))
def P(s,style='Bodyx'): return Paragraph(s,styles[style])
def footer(canvas,doc):
    canvas.saveState(); w,h=letter
    canvas.setStrokeColor(colors.HexColor('#E5EAF4')); canvas.line(0.65*inch,0.54*inch,w-0.65*inch,0.54*inch)
    canvas.setFont('Segoe',7.5); canvas.setFillColor(colors.HexColor(MUTED)); canvas.drawString(.68*inch,.36*inch,'ArthiX  •  Product overview')
    canvas.drawRightString(w-.68*inch,.36*inch,f'{doc.page}')
    canvas.restoreState()
story=[]
story += [Spacer(1,.18*inch),P('ArthiX','Hero'),P('A practical AI-enabled back office for growing teams','Deck')]
hero=Table([[P('<b>One workspace.</b><br/>The everyday work of running a business, brought together.','Deck'),P('CRM  ·  Finance  ·  People  ·  Operations','Smallx')]],colWidths=[3.7*inch,2.55*inch],rowHeights=[1.12*inch])
hero.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#EEF2FF')),('BOX',(0,0),(-1,-1),0,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),18),('RIGHTPADDING',(0,0),(-1,-1),18)])); story += [hero,Spacer(1,.26*inch),P('What ArthiX is','H2x'),P('ArthiX is an open-source, self-hosted business platform that brings core company operations into one place. Teams can work with shared records, operational dashboards, and assisted workflows instead of spreading work across disconnected tools.','Bodyx'),P('The experience is designed to make common work easier to see and act on: track customer relationships, manage invoices and expenses, organize people and inventory, follow support requests, and keep an eye on approvals. AI assistance can help interpret requests and suggest next steps when configured.','Bodyx'),P('A connected workspace for the work behind the business','Quote')]
cards=[[P('<b>Customer work</b><br/>CRM records, deals, and follow-ups','Bodyx'),P('<b>Money work</b><br/>Invoices, expenses, budgets, and approvals','Bodyx')],[P('<b>Team work</b><br/>People, payroll, projects, and schedules','Bodyx'),P('<b>Operations</b><br/>Inventory, vendors, support, and workflows','Bodyx')]]
t=Table(cards,colWidths=[3.12*inch]*2,rowHeights=[.76*inch]*2); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor(PALE)),('INNERGRID',(0,0),(-1,-1),5,colors.white),('BOX',(0,0),(-1,-1),0,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),12)])); story += [t,PageBreak()]
story += [P('How teams use it','H2x'),P('A shared dashboard gives a starting point for reviewing activity and moving into the work that needs attention. Each area keeps related records and actions close together.','Bodyx')]
rows=[[P('<b>Customer relationships</b><br/>Keep companies, contacts, opportunities, and activity organized.','Bodyx'),P('<b>Finance and approvals</b><br/>Review invoices, expenses, budgets, and requests in a consistent workflow.','Bodyx')],[P('<b>People and projects</b><br/>Coordinate team information, work, and schedules from shared records.','Bodyx'),P('<b>Service and operations</b><br/>Follow customer support, products, inventory, vendors, and internal tasks.','Bodyx')],[P('<b>Automation and AI</b><br/>Use configurable workflows and optional AI assistance to reduce repetitive steps.','Bodyx'),P('<b>Integrations</b><br/>Connect external services where a supported integration is configured.','Bodyx')]]
t=Table(rows,colWidths=[3.12*inch]*2,rowHeights=[.82*inch]*3); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F5F7FB')),('INNERGRID',(0,0),(-1,-1),5,colors.white),('BOX',(0,0),(-1,-1),0,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13)])); story += [t,Spacer(1,.18*inch),P('Example: StrideWorks Footwear','H3x'),P('The included sample business demonstrates how a small footwear retailer can organize its company profile, customers, products, sales activity, and day-to-day operations. Demo records are illustrative and should not be treated as real business data.','Bodyx'),P('Getting started','H2x'),P('Run the project using the repository’s Docker Compose setup, open the local admin site, and load the provided demo dataset when you want sample records. AI features require an AI provider to be configured; the core workspace can be explored without one.','Bodyx'),P('For the current setup commands, configuration, and demo sign-in, use the project README and local environment values. Change any demo credentials before exposing a deployment beyond your machine.','Smallx'),PageBreak()]
story += [P('Under the hood','H2x'),P('ArthiX is organized as a modular web application with an API, a browser-based admin interface, a relational database, and supporting services. The project includes packages for shared business logic and integrations. Its self-hosted setup keeps deployment under the operator’s control.','Bodyx')]
arch=Table([[P('ADMIN WEB','Smallx'),P('API','Smallx'),P('BUSINESS DATA','Smallx')],[P('<b>Next.js</b><br/>Dashboard and workflows','Bodyx'),P('<b>Hono / Node.js</b><br/>Business endpoints','Bodyx'),P('<b>PostgreSQL</b><br/>Records and relationships','Bodyx')],[P('User experience','Smallx'),P('Rules and integrations','Smallx'),P('Redis support service','Smallx')]],colWidths=[2.08*inch]*3,rowHeights=[.36*inch,.74*inch,.38*inch]); arch.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F1F4FB')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8EDFF')),('INNERGRID',(0,0),(-1,-1),3,colors.white),('BOX',(0,0),(-1,-1),0,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),11)])); story += [arch,Spacer(1,.18*inch),P('Deployment notes','H3x'),P('The project is intended to be self-hosted. Set secrets and service credentials for real deployments, keep the database and API private behind your chosen network boundary, and configure backups and integrations for your environment. The exact options are documented in the repository’s environment example.','Bodyx'),P('A note on AI','H3x'),P('AI-assisted features depend on a configured provider, network access, and valid credentials. AI output should be reviewed by a person before it is used for consequential business decisions.','Bodyx'),Spacer(1,.16*inch),P('ArthiX brings the company’s everyday work into a workspace teams can understand, adapt, and run themselves.','Quote'),P('This overview describes the project based on the workspace documentation and configuration. Feature availability can depend on the deployed version and integrations.','Smallx')]
doc=SimpleDocTemplate(str(PDF),pagesize=letter,rightMargin=.68*inch,leftMargin=.68*inch,topMargin=.64*inch,bottomMargin=.72*inch,title='ArthiX Product Overview',author='ArthiX')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

# Short 8-scene narration: warm, clear en-IN neural voice. The complete narration
# appears on screen in concise timed captions; the spoken track carries the detail.
SCENES=[
('A calmer way to run the business','Running a business means keeping track of a hundred moving parts. Customer conversations, money, people, and daily operations often end up scattered across different tools. ArthiX brings that work into one clear, connected workspace.'),
('Meet ArthiX','ArthiX is an open-source, self-hosted business platform for growing teams. It gives your company a shared place to organize its everyday work, see what needs attention, and move from information to action.'),
('See the whole picture','Start from the dashboard. Get a quick sense of what is happening, then move into the details behind each number. Shared records help your team keep context close, so the next step is easier to find.'),
('Build better customer relationships','In customer management, keep companies, people, opportunities, and activity together. Your team can follow a relationship from the first conversation through ongoing work, with useful details in one place.'),
('Keep operations moving','ArthiX also brings together finance, people, projects, service, inventory, and vendors. Handle recurring business tasks from focused workspaces, and use approvals to give important decisions a clear path.'),
('Make repeat work easier','Configurable workflows help automate routine steps. Optional AI assistance can help draft, summarize, and suggest next actions. Your team stays in control and reviews the work before it matters.'),
('Explore with a sample company','The StrideWorks Footwear demo shows how a small retailer can use ArthiX to organize customers, products, sales, and operations. It is a safe way to explore the product and see how the pieces fit together.'),
('Your business, in one workspace','ArthiX is designed for teams who want a practical business platform they can understand and run themselves. Start with the work you need today, shape the setup for your company, and grow from there. ArthiX. One workspace for the work behind your business.')]
W,H=1280,720
FONT='C:/Windows/Fonts/segoeui.ttf'; BOLD='C:/Windows/Fonts/segoeuib.ttf'
def f(size,b=False): return ImageFont.truetype(BOLD if b else FONT,size)
def make_scene(i,title,script):
    im=Image.new('RGB',(W,H)); px=im.load()
    c1=(14,21,43); c2=(38,52,103)
    for y in range(H):
        for x in range(W):
            t=(.65*x/W+.35*y/H); glow=max(0,1-math.sqrt(((x-980)/950)**2+((y-120)/700)**2))
            px[x,y]=tuple(int(c1[k]*(1-t)+c2[k]*t+glow*[14,40,48][k]) for k in range(3))
    d=ImageDraw.Draw(im,'RGBA'); d.ellipse((870,-170,1440,390),fill=(91,124,250,24)); d.ellipse((-200,510,320,1030),fill=(72,213,206,18))
    d.rounded_rectangle((64,58,185,98),20,fill=(255,255,255,22),outline=(255,255,255,40)); d.text((86,67),'ARTHIX',font=f(18,True),fill=(255,255,255,240))
    d.text((64,178),f'{i+1:02d}  /  08',font=f(16,True),fill=(72,213,206,255))
    # Left typographic statement
    for idx,line in enumerate(textwrap.wrap(title,22)):
        d.text((64,226+idx*65),line,font=f(48,True),fill=(255,255,255,255))
    # Narration caption, max 5 lines
    caption=' '.join(script.split())
    lines=[]; words=caption.split(); cur=''
    for word in words:
        test=(cur+' '+word).strip()
        if d.textbbox((0,0),test,font=f(22))[2]>535:
            lines.append(cur); cur=word
        else: cur=test
    if cur: lines.append(cur)
    lines=lines[:6]
    d.rounded_rectangle((64,440,642,640),18,fill=(6,11,27,105),outline=(255,255,255,25),width=1)
    for j,line in enumerate(lines): d.text((86,464+j*28),line,font=f(18),fill=(229,235,249,245))
    # Right-side crafted app visualization; reusable branded dashboard card.
    d.rounded_rectangle((700,130,1216,616),28,fill=(248,250,255,255),outline=(255,255,255,100),width=1)
    d.rounded_rectangle((700,130,1216,190),28,fill=(255,255,255,255)); d.rectangle((700,160,1216,190),fill=(255,255,255,255))
    d.text((728,151),'ArthiX',font=f(21,True),fill=(24,35,59,255)); d.text((1082,156),'●  Workspace',font=f(12),fill=(99,112,139,255))
    d.rounded_rectangle((728,214,1188,285),16,fill=(238,242,255,255)); d.text((750,229),'YOUR BUSINESS, IN FOCUS',font=f(12,True),fill=(91,124,250,255)); d.text((750,251),['Today at a glance','Everything in one place','Clear view, next step','Customer relationships','Operations overview','Workflow automation','StrideWorks Footwear','Built for your team'][i],font=f(20,True),fill=(24,35,59,255))
    # KPI cards
    for j,(label,val) in enumerate([('CUSTOMERS','248'),('OPEN ITEMS','12'),('THIS MONTH','$18.4k')]):
        x=728+j*150; d.rounded_rectangle((x,305,x+138,378),12,fill=(247,248,252,255),outline=(231,235,244,255)); d.text((x+12,318),label,font=f(10,True),fill=(99,112,139,255)); d.text((x+12,339),val,font=f(21,True),fill=(24,35,59,255))
    # chart bars and activity list
    d.text((730,400),'Activity',font=f(15,True),fill=(24,35,59,255)); d.text((1082,403),'This week  ›',font=f(11),fill=(91,124,250,255))
    d.line((730,548,1187,548),fill=(226,231,241,255),width=1)
    for j,hb in enumerate([35,55,48,83,68,103,91,126]):
        x=752+j*49; d.rounded_rectangle((x,540-hb,x+24,540),6,fill=((91,124,250,255) if j==6 else (91,124,250,120)))
    d.text((730,565),'MON      TUE      WED      THU      FRI      SAT      SUN',font=f(10),fill=(120,130,153,255))
    # progress accent
    d.rounded_rectangle((64,673,1216,677),2,fill=(255,255,255,28)); d.rounded_rectangle((64,673,64+(i+1)*144,677),2,fill=(72,213,206,220))
    im.save(TMP/f'scene_{i:02d}.png')

async def narrate():
    voice='en-IN-NeerjaNeural'
    for i,(_,script) in enumerate(SCENES):
        comm=edge_tts.Communicate(script,voice,rate='+15%',volume='+0%')
        await comm.save(str(TMP/f'voice15_{i:02d}.mp3'))
if not all((TMP/f'voice15_{i:02d}.mp3').exists() for i in range(8)):
    asyncio.run(narrate())
for i,(title,script) in enumerate(SCENES): make_scene(i,title,script)

# Build a scene-timed, full-HD, voice-led promo using gentle crossfades and slow motion.
ff=Path(__import__('imageio_ffmpeg').get_ffmpeg_exe())
durations=[]
for i in range(len(SCENES)):
    p=subprocess.run([str(ff),'-i',str(TMP/f'voice15_{i:02d}.mp3'),'-f','null','-'],capture_output=True,text=True)
    import re
    m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',p.stderr)
    durations.append(int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))+.9)
inputs=[]; filterparts=[]
for i,dur in enumerate(durations):
    inputs += ['-loop','1','-t',f'{dur:.2f}','-i',str(TMP/f'scene_{i:02d}.png')]
    filterparts.append(f'[{i}:v]scale=1280:720,fps=24,trim=duration={dur:.2f},settb=AVTB,setpts=PTS-STARTPTS,format=yuv420p,fade=t=in:st=0:d=0.45,fade=t=out:st={dur-.45:.2f}:d=0.45[v{i}]')
filterparts.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[slides]')
audio_inputs=[]
for i in range(8): audio_inputs+=['-i',str(TMP/f'voice15_{i:02d}.mp3')]
abase=len(SCENES)
concat=''.join(f'[{abase+i}:a]' for i in range(8))+'concat=n=8:v=0:a=1[aout]'
filterparts.append(concat)
cmd=[str(ff),'-y','-hide_banner','-loglevel','error',*inputs,*audio_inputs,'-filter_complex',';'.join(filterparts),'-map','[slides]','-map','[aout]','-t','120','-c:v','libx264','-preset','ultrafast','-crf','23','-r','24','-c:a','aac','-b:a','192k','-movflags','+faststart',str(VIDEO)]
subprocess.run(cmd,check=True)
print(f'PDF={PDF}\nVIDEO={VIDEO}\nVOICE_SECONDS={sum(durations):.1f}\nSCENE_SECONDS={[round(x,1) for x in durations]}')
