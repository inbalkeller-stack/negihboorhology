import json,re,os,glob,base64,io,sys
from PIL import Image
T='/root/.claude/projects/-home-claude/c40fb6e0-d632-50f1-a126-511c66777995/tool-results'
A='/home/claude/negihboorhology/site/assets'
for f in sorted(glob.glob(T+'/*'),key=os.path.getmtime):
    raw=open(f,encoding='utf-8',errors='ignore').read()
    if 'TAG=' not in raw: continue
    try: raw=''.join(x.get('text','') for x in json.loads(raw))
    except Exception: pass
    for m in re.finditer(r'TAG=([\w/.-]+)\|CHUNK0\|data:image/\w+;base64,([A-Za-z0-9+/=]+)\|END',raw):
        rel,b=m.group(1),base64.b64decode(m.group(2))
        out=os.path.join(A,rel); os.makedirs(os.path.dirname(out),exist_ok=True)
        if os.path.exists(out) and os.path.getmtime(out)>os.path.getmtime(f): continue
        open(out,'wb').write(b); im=Image.open(io.BytesIO(b))
        print(rel,im.size,im.mode,f'{len(b)//1024}KB')
