#!/usr/bin/env python3
"""Rebuilds the figure layer of the Figma frame "mobile version" (296:367, 393x852) and renders it
to site/assets/img/cover-mobile.webp (transparent, 3x). Values copied from Figma's design context."""
import asyncio, os
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "mobile-src")
OUT = os.path.join(HERE, "..", "site", "assets", "img", "cover-mobile.webp")

def I(h): return f"file://{SRC}/{h}.webp"
F = "4ece066de987599f7378b6277190d952ea0a23a9"
# (box left, top, w, h, inner-transform or None, inner w, inner h, image id, crop) ; crop = (h%, left%, top%, w%) or None (=cover)
L = [
 (2,42,133,191,None,0,0,"4ece066de987599f7378b6277190d952ea0a23a9",None),
 (43,158,133,191,None,0,0,"34e43fbf8471c6c48ffd9a3fa1f20eec206fa8a2",None),
 (142,-47,133,191,None,0,0,"d3f5f8010fba10ca8c49feb79c88b1904b00eda1",None),
 (113,434,139,200,None,0,0,"7b20c5b8166c9aed140555633092f35c57632c1c",None),
 (290,233,133,192,None,0,0,"5c162da3dcc13deacd50e60aeabce26d6624ee74",None),
 (110,85,133,191,None,0,0,"d5ccb1be0b54b78cc4506c1f94eb0a24ac929cec",None),
 (220,383,133,192,None,0,0,"62a2660cfb5f7c628fa1c6a064b670bd442394d2",None),
 (280,186,133,191,None,0,0,"a0d6e209ca121785faf0c552485f739bf81aafdb",None),
 (6,462,145,144,None,0,0,"05d267bce78a72d63bd5e0f2ae6ea310bd59880f",None),
 (263,539,116,115,None,0,0,"b4a700531fb7975de64d89221f938746cd475749",None),
 (9,572,150,149,None,0,0,"bbf5f017a9ca37653c51e143ab015bde75acefdf",None),
 (-17,766,111,110,None,0,0,"ce4815191d67dbb6fb6c736c1ad9891fe53927da",None),
 (2,633,73,72,None,0,0,"1d78b7daf2f1b33ee4d04423a741c9b56f5a4ccd",None),
 (293,144,99,98,None,0,0,"df3f28e5a59722c7e7a51769c010fce68431fa8c",None),
 (262,712,66,61,None,0,0,"05b11355ce83cc1bdad80d9f1c3f38fb8b63afcc",(268.66,-73.67,-111.94,173.73)),
 (75,22,88,136,"rotate(180deg) scaleY(-1)",88,136,"f20348a8da619f9c8ea6a80c543b9fb967509c13",(170.59,-83.08,-70.59,183.2)),
 (137.99,769.15,52.027,67.699,"rotate(-14.75deg)",38,60,"f20348a8da619f9c8ea6a80c543b9fb967509c13",(386.67,-218.71,-165,424.26)),
 (136,668,80,79,None,0,0,"8f3f67a845732c9061965cfb3b6a6c1f895eb9e9",None),
 (262,784,108,57,"rotate(180deg) scaleY(-1)",108,57,"33eaa038682b463e3bd6bdb0b42d70cd29c55758",(403.94,-48.15,-172.14,148.15)),
 (277.87,640.62,127.255,84.751,"rotate(-168.12deg) scaleY(-1)",117,62,"33eaa038682b463e3bd6bdb0b42d70cd29c55758",(403.94,-48.15,-172.14,148.15)),
 (290,289,160,230,"rotate(180deg) scaleY(-1)",160,230,"33eaa038682b463e3bd6bdb0b42d70cd29c55758",None),
 (134,590,82,81,None,0,0,"e72d0d3344c75069a05fd2f1463459ca430cf229",None),
 (227,84,106,105,None,0,0,"cfe809977612ad44419930fd54fcb8adbb501615",None),
 (295,32,130,129,None,0,0,"8fa5df5852254baf6b7d5550947a762a1000505a",None),
 (10,543,88,88,"rotate(180deg) scaleY(-1)",88,88,"5f39ad3c5be90ffad0265cf3cd9f6bc46ff50e02",None),
 (-12,288,100,99,None,0,0,"f6b64870d4ce3231cb9e7816037cf13375dadcc7",None),
 (217,166,83,118,None,0,0,"49d03017dcf9ba39436267579f3346c71a8e376e",(266.1,-53.13,-85.59,262.9)),
 (170,603,121.217,155.523,"rotate(169.34deg) scaleY(-1)",97,140,"692d5a64732e47e8cd76585ab891b06fa5f0fc30",None),
 (241,-13,113,163,None,0,0,"3e3c0796fdad427a6459dc7873e7c5f55c901084",None),
 (286,413,135,151,None,0,0,"d95080b0d9a76c41b2f4c4d8db29a694d3faa925",(129.14,-0.19,0,100.38)),
 (216,753,68,99,None,0,0,"36a4859025f668b88ffcb74e9b5013e31d8a6c0f",None),
 (-29,425,87,181,"rotate(180deg) scaleY(-1)",87,181,"091e9d433606e65a23473dc639d3a0dd06bcde55",(100,-109.26,0,209.32)),
 (-17,338,121,88,None,0,0,"01ab621aba705e4166c6d6e44c04a3ccbe2edfd1",(165.89,-0.09,0,120.96)),
 (-7,206,70,69,"rotate(180deg) scaleY(-1)",70,69,"8c4f966db95d03d012903b523b084b95aa28e30c",None),
 (0,681,157,156,None,0,0,"f09e4bb11f7c1724013c2fd6eda1fe45d07f62a6",None),
 (15,446,65,65,None,0,0,"8653517d92b74387ac830b14c935e542aa3ed613",None),
 (-47,10,127,109,None,0,0,"7041371423aa1330ecb7337c189f8933dc40bf6c",(159.63,-0.03,0,137.85)),
 (60,554,119,118,None,0,0,"d5c9b3af194183a7c6a0d68d83dba8325aebdd6f",None),
 (321,713,91,63,None,0,0,"b3e713b235f2531c250fc6a534b74ad80297dfcf",(184.58,-28.57,-0.23,128.57)),
 (121,100,148,147,None,0,0,"8fe6426720af040e6fad65c45f0ad9cd6ab0c01e",None),
 (70,-9,117,123,None,0,0,"091e9d433606e65a23473dc639d3a0dd06bcde55",(147.15,-55.6,0,155.65)),
 (157,405,254.205,347.745,"rotate(-175.8deg) scaleY(-1)",230.55,331.767,"f20348a8da619f9c8ea6a80c543b9fb967509c13",None),
 # drawn above the title in Figma (no overlap with it)
 (53,114,133,130,"rotate(180deg) scaleY(-1)",133,130,"fd4753696b57d6eef8c034b37964a6786c8777c3",(147.22,0,-47.07,100)),
]

def img(h, crop):
    if crop is None:
        return f'<img src="{I(h)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
    hh, l, t, w = crop
    return (f'<div style="position:absolute;inset:0;overflow:hidden"><img src="{I(h)}" style="position:absolute;'
            f'height:{hh}%;left:{l}%;top:{t}%;width:{w}%;max-width:none"></div>')

parts = []
for (x, y, w, h, tr, iw, ih, hid, crop) in L:
    if tr:
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center">'
                     f'<div style="flex:none;transform:{tr}"><div style="position:relative;width:{iw}px;height:{ih}px">{img(hid, crop)}</div></div></div>')
    else:
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{img(hid, crop)}</div>')
html = ('<!doctype html><html><head><style>html,body{margin:0;background:transparent}'
        '#f{position:relative;width:393px;height:852px;overflow:hidden}</style></head><body><div id="f">'
        + "".join(parts) + '</div></body></html>')
open(os.path.join(HERE, "mobile-figures.html"), "w").write(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 393, "height": 852}, device_scale_factor=3)
        await pg.goto("file://" + os.path.join(HERE, "mobile-figures.html"))
        await pg.wait_for_load_state("networkidle")
        png = os.path.join(HERE, "mobile-figures.png")
        await pg.locator("#f").screenshot(path=png, omit_background=True)
        # preview on red for checking
        await pg.add_style_tag(content="body{background:#bd2429}")
        await pg.locator("#f").screenshot(path=os.path.join(HERE, "mobile-figures-preview.png"))
        await b.close()
    from PIL import Image
    im = Image.open(png); im.save(OUT, "WEBP", quality=86, method=6)
    print(OUT, im.size, os.path.getsize(OUT)//1024, "KB")
asyncio.run(main())
