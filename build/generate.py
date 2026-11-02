#!/usr/bin/env python3
"""Generates the static site for שכונולוגיה from the Figma layout data.
All coordinates are Figma pixels on the 1728px-wide frames."""
import os, json, html

OUT = os.path.join(os.path.dirname(__file__), "..", "site")
SITE_TITLE = "שכונולוגיה"
DESC = "שכונולוגיה – ספר מאויר על שכונות תל אביב. איורים: ענבל קלר."

# Order = nav order (right to left) = reading order of the book.
PAGES = [
    {"slug": "neve-sharet", "nav": "נווה שרת/שיכון דן", "title": "נווה שרת ושיכון דן", "h": 2444, "map_rot": 0,
     "labels": [
        {"name": "נווה שרת", "panel": "neve-sharet", "box": (1434, -53, 345, 343), "text": (1589.5, 104)},
        {"name": "נווה דן", "panel": "neve-dan", "box": (-26, 2212, 333, 330), "text": (120.5, 2364)},
     ]},
    {"slug": "ramat-aviv", "nav": "רמת אביב/כוכב הצפון", "title": "רמת אביב וכוכב הצפון", "h": 2473, "map_rot": 0,
     "labels": [
        {"name": "רמת אביב", "panel": "ramat-aviv", "box": (1446, -50, 350, 348), "text": (1602.5, 113)},
        {"name": "כוכב הצפון", "panel": "kochav-hatzafon", "box": (-24, 2206, 362, 360), "text": (134, 2373)},
     ]},
    {"slug": "old-north", "nav": "הצפון הישן", "title": "הצפון הישן", "h": 2444, "map_rot": 0,
     "labels": [
        {"name": "הצפון הישן", "panel": "old-north", "box": (1438, 48, 362, 360), "text": (1604.5, 219)},
     ]},
    {"slug": "lev-tlv", "nav": "לב ת״א", "title": "לב תל אביב", "h": 2445, "map_rot": 0,
     "labels": [
        {"name": "לב תל אביב", "panel": "lev-tlv", "box": (1385, -51, 371, 369), "text": (1551.5, 119)},
     ]},
    {"slug": "florentin", "nav": "פלורנטין", "title": "פלורנטין", "h": 2444, "map_rot": 0,
     "labels": [
        {"name": "פלורנטין", "panel": "florentin", "box": (1402, -71, 388, 386), "text": (1575.5, 108)},
     ]},
    {"slug": "neve-shaanan", "nav": "נווה שאנן", "title": "נווה שאנן", "h": 2444, "map_rot": 0,
     "labels": [
        {"name": "נווה שאנן", "panel": "neve-shaanan", "box": (1382, -43, 397, 394), "text": (1557.5, 138)},
     ]},
    {"slug": "yad-eliyahu", "nav": "יד אליהו/התקווה", "title": "יד אליהו והתקווה", "h": 2442, "map_rot": 0,
     # the woman with the pink trolley was cut in the map art; her full drawing sits on top (% of the map)
     "patches": [{"src": "img/hatikva-woman.webp", "left": 20.4164, "top": 58.6978, "width": 3.6088}],
     "labels": [
        {"name": "יד אליהו", "panel": "yad-eliyahu", "box": (1379, -47, 380, 378), "text": (1548.5, 123)},
        {"name": "התקווה", "panel": "hatikva", "box": (-34, 2156, 420, 417), "text": (151.5, 2352)},
     ]},
    {"slug": "shapira", "nav": "שפירא/קריית שלום", "title": "שפירא וקריית שלום", "h": 2444, "map_rot": 0,
     "labels": [
        {"name": "שפירא", "panel": "shapira", "box": (1429, -74, 373, 371), "text": (1593.5, 95)},
        {"name": "קריית שלום", "panel": "kiryat-shalom", "box": (-1, 2168, 381, 379), "text": (168.5, 2343), "wrap": True},
     ]},
]

# Sticker image boxes inside the 1147x1140 "דמויות 8 2" component (from Figma insets: top right bottom left)
DEFAULT_INSET = (0.2447, 0.1988, 0.3579, 0.1212)
HOVER_INSET = (0.2649, 0.2127, 0.3596, 0.0915)

def inset_box(box, inset):
    x, y, w, h = box
    t, r, b, l = inset
    return (x + l * w, y + t * h, w * (1 - l - r), h * (1 - t - b))

def r2(v):
    return round(v, 1)

def head(title, depth, extra_class=""):
    p = "../" * depth
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(DESC)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(DESC)}">
<meta property="og:image" content="{p}assets/img/og.jpg">
<meta name="theme-color" content="#bd242a">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/style.css">
</head>
<body class="{extra_class}">
"""

def nav(depth, current=None):
    p = "../" * depth
    items = []
    for pg in PAGES:
        cur = ' aria-current="page"' if pg["slug"] == current else ""
        items.append(f'<li><a href="{p}{pg["slug"]}/"{cur}>{html.escape(pg["nav"])}</a></li>')
    # arrow: on the home page it opens the first neighbourhood; everywhere else it goes home
    if current is None:
        nxt, label = f'{p}{PAGES[0]["slug"]}/', "לשכונה הראשונה"
    else:
        nxt, label = f'{p}', "חזרה לעמוד הראשי"
    items.append(f'<li><a class="nav-next" href="{nxt}" aria-label="{label}" title="{label}">&larr;</a></li>')
    home = "" if current is None else f'<a class="nav-home" href="{p}" aria-label="עמוד ראשי" title="עמוד ראשי">{SITE_TITLE}</a>'
    return f'<nav class="nav" aria-label="שכונות">{home}<ul>{"".join(items)}</ul></nav>'

def dialog(depth):
    return """
<dialog class="panel-dialog" id="panel-dialog" aria-label="נתוני השכונה">
  <button class="dialog-close" type="button" aria-label="סגירה"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M5 5L19 19M19 5L5 19" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg></button>
  <img class="panel-img" alt="">
</dialog>
"""

FOOT = '<script src="{p}assets/js/main.js" defer></script>\n</body>\n</html>\n'


# ---- Loading animation (Figma frames "מסך ראשי" 10:126 → 10:937) ----
# Each burst: number in Figma -> (x, y) on the 1728x1117 frame. Size 317x325.
BURSTS = {1:(33,33),2:(406,645),3:(978,113),4:(565,150),5:(954,691),6:(1250,320),7:(819,378),8:(407,378),
  9:(705,758),10:(134,528),11:(134,808),12:(1271,596),13:(1439,119),14:(736,49),15:(578,528),16:(192,216),
  17:(384,0),18:(1347,815),19:(1054,444),20:(1454,406),21:(-47,282),22:(623,374),23:(1213,113),24:(828,559),
  25:(564,-56),26:(312,807),27:(-47,644),28:(1526,644),29:(542,815),30:(1052,792),31:(911,-40),32:(270,445),
  33:(247,-12),34:(1077,308),35:(-24,853),36:(75,374),37:(1070,646),38:(810,234),39:(876,853),40:(1463,853),
  41:(1122,-3),42:(38,-96)}
# which frame of the sequence each burst first appears in
STEPS = [[3],[6],[1,2,7,8,9,4,5],[10,11,12],[13,14,15],[16,17,18],[19,20,21],[22,23,24,25,26,27,28],
         list(range(29,43))]
# stacking order in the final frame (bottom -> top)
Z_ORDER = [1,2,3,7,8,9,29,30,31,32,33,34,35,36,10,11,12,19,20,21,16,17,18,37,38,13,14,15,4,5,39,40,41,42,6,
           22,23,24,25,26,27,28]
BUTTONS_STEP = 5  # the אודות / התחלה / מאת buttons appear with the 6th frame

def build_intro():
    step_of = {n: i for i, st in enumerate(STEPS) for n in st}
    order_in_step = {n: st.index(n) for st in STEPS for n in st}
    imgs = []
    for n in Z_ORDER:
        x, y = BURSTS[n]
        imgs.append(f'<img class="burst" src="assets/img/burst.webp" alt="" '
                    f'style="--x:{x};--y:{y};--step:{step_of[n]};--k:{order_in_step[n]}">')
    return f"""<div class="intro" id="intro" role="dialog" aria-modal="true" hidden aria-label="{SITE_TITLE}" style="--steps:{len(STEPS)};--buttons-step:{BUTTONS_STEP}">
  <div class="intro-stage">
    <p class="intro-title">{SITE_TITLE}</p>
    {''.join(imgs)}
  </div>
  <div class="intro-buttons">
    <button class="intro-btn small" type="button" data-dialog="about-dialog">אודות</button>
    <a class="intro-btn start" id="intro-start" href="{PAGES[0]["slug"]}/">התחלה</a>
  </div>
</div>
"""

def build_home():
    h = head(SITE_TITLE, 0, "home")
    h += build_intro()
    h += f"""<main class="cover">
  <img class="cover-bg" src="assets/img/cover.webp" alt="" fetchpriority="high">
  <button class="corner-btn corner-about" type="button" data-dialog="about-dialog">אודות</button>
  <div class="cover-center">
    <h1 class="cover-title" id="cover-title" tabindex="0" role="button" aria-controls="intro">{SITE_TITLE}</h1>
    {nav(0)}
  </div>
</main>

<dialog class="info-dialog about" id="about-dialog" aria-labelledby="about-title">
  <button class="dialog-close" type="button" aria-label="סגירה"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M5 5L19 19M19 5L5 19" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" fill="none"/></svg></button>
  <div class="info-body">
    <p class="strong" id="about-title">איורים מאת ענבל קלר.</p>
    <p class="strong">הופק במסגרת קורס איור ספרים בהנחיית נעמה בנזימן,</p>
    <p class="strong">המכון הטכנולוגי חולון hit.</p>
    <p>כלל הנתונים נלקחו מאתר open data של עיריית תל אביב.</p>
    <p>טיפוגרפיה: היציאה הבאה, מאת הגילדה</p>
  </div>
</dialog>
"""
    h += FOOT.format(p="")
    return h

def build_page(pg):
    d = 1
    p = "../"
    out = head(f'{pg["title"]} | {SITE_TITLE}', d, "map-page")
    out += f'<main class="stage" style="--fh:{pg["h"]}">\n'
    out += "  " + nav(d, pg["slug"]) + "\n"
    out += f'  <h1 class="sr-only">{html.escape(pg["title"])}</h1>\n'
    out += '  <div class="canvas">\n'
    out += f'  <img class="map" src="{p}assets/maps/{pg["slug"]}.webp" alt="מפה מאוירת של {html.escape(pg["title"])}" width="1728" height="{pg["h"]}">\n'
    for pt in pg.get("patches", []):
        out += (f'  <img class="patch" src="{p}assets/{pt["src"]}" alt="" '
                f'style="left:{pt["left"]}%;top:{pt["top"]}%;width:{pt["width"]}%">\n')
    for lb in pg["labels"]:
        bx, by, bw, bh = inset_box(lb["box"], DEFAULT_INSET)
        hx, hy, hw, hh = inset_box(lb["box"], HOVER_INSET)
        tx, ty = lb["text"]
        style = f'--x:{r2(bx)};--y:{r2(by)};--w:{r2(bw)};--h:{r2(bh)}'
        hstyle = f'--x:{r2(hx-bx)};--y:{r2(hy-by)};--w:{r2(hw)};--h:{r2(hh)}'
        tstyle = f'--x:{r2(tx-bx)};--y:{r2(ty-by)}'
        wrap = " wrap" if lb.get("wrap") else ""
        out += (f'  <button class="label" type="button" style="{style}" '
                f'data-panel="{p}assets/panels/{lb["panel"]}.webp" data-name="{html.escape(lb["name"])}" '
                f'aria-haspopup="dialog" aria-label="נתוני {html.escape(lb["name"])}">\n'
                f'    <img class="sticker" src="{p}assets/img/label.webp" alt="">\n'
                f'    <img class="sticker-hover" src="{p}assets/img/label-hover.webp" alt="" style="{hstyle}">\n'
                f'    <span class="label-text{wrap}" style="{tstyle}">{html.escape(lb["name"])}</span>\n'
                f'  </button>\n')
    out += '  </div>\n'
    # phones: the map labels get small, so the stats also open from big buttons under the map
    out += '  <div class="stats-bar">\n'
    for lb in pg["labels"]:
        out += (f'    <button class="stats-btn" type="button" data-panel="{p}assets/panels/{lb["panel"]}.webp" '
                f'data-name="{html.escape(lb["name"])}" aria-haspopup="dialog">'
                f'<span>{html.escape(lb["name"])}</span><small>נתוני השכונה</small></button>\n')
    out += '  </div>\n</main>\n'
    out += dialog(d)
    out += FOOT.format(p=p)
    return out

def build_404():
    out = head(f"הדף לא נמצא | {SITE_TITLE}", 0, "home")
    out = out.replace('href="assets/', 'href="/negihboorhology/assets/')
    out += f"""<main class="cover">
  <img class="cover-bg" src="/negihboorhology/assets/img/cover.webp" alt="">
  <div class="cover-center">
    <h1 class="cover-title small">הדף לא נמצא</h1>
    <p class="notfound"><a href="/negihboorhology/">חזרה לעמוד הראשי</a></p>
  </div>
</main>
</body>
</html>
"""
    return out

def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    write("index.html", build_home())
    for pg in PAGES:
        write(f'{pg["slug"]}/index.html', build_page(pg))
    write("404.html", build_404())
    print("ok")
