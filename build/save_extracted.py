#!/usr/bin/env python3
"""Decode an image extracted from Figma (tool-result JSON containing a data URL) into site/assets.
Usage: save_extracted.py <tool-result-file> <site-relative-output.webp>"""
import json, base64, re, sys, os, io
from PIL import Image
src, rel = sys.argv[1], sys.argv[2]
raw = open(src, encoding='utf-8').read()
try:
    raw = ''.join(x.get('text', '') for x in json.loads(raw))
except Exception:
    pass
m = re.search(r'data:image/(\w+);base64,([A-Za-z0-9+/=]+)', raw)
data = base64.b64decode(m.group(2))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'assets', rel)
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'wb').write(data)
im = Image.open(io.BytesIO(data))
print(rel, im.size, im.mode, f'{len(data)//1024}KB')
