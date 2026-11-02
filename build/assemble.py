#!/usr/bin/env python3
"""Stitch base64 chunks pulled from Figma's local image server into one image.
Usage: assemble.py <site-relative-output> <result-file> [<result-file> ...]
Each result file holds 'CHUNKn|<base64...>|END'. The newest file wins for a given n."""
import json, re, sys, os, io, base64, glob
from PIL import Image
rel, files = sys.argv[1], sys.argv[2:]
parts = {}
for f in sorted(files, key=os.path.getmtime):
    raw = open(f, encoding='utf-8').read()
    try: raw = ''.join(x.get('text', '') for x in json.loads(raw))
    except Exception: pass
    for m in re.finditer(r'CHUNK(\d+)\|(.*?)\|END', raw, re.S):
        parts[int(m.group(1))] = m.group(2)
n = max(parts) + 1
missing = [i for i in range(n) if i not in parts]
assert not missing, f'missing chunks {missing}'
url = ''.join(parts[i] for i in range(n))
b64 = url.split('base64,', 1)[1]
data = base64.b64decode(b64)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'assets', rel)
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'wb').write(data)
im = Image.open(io.BytesIO(data)); im.load()
print(rel, im.size, im.mode, f'{len(data)//1024}KB', f'from {n} chunks')
