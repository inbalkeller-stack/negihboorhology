#!/usr/bin/env python3
"""Turn the PNGs exported from Figma into web-ready WebP files in site/assets.

Usage:  python3 prepare_assets.py <folder-with-figma-exports>

Matches Figma layer names (as exported, e.g. "נווה שרת טקסט 1@2x.png") to the
site's file names, resizes and converts to WebP. Run again any time the art changes.
"""
import sys, os, re, unicodedata
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "site", "assets")

# layer name (without "@2x" / extension)  ->  output path inside site/assets
MAPS = {
    "נווה שרת ושיכון דן1 1": "maps/neve-sharet.webp",
    "כוכב הצפון ורמתאביב 1": "maps/ramat-aviv.webp",
    "הצפון הישן 2": "maps/old-north.webp",
    "לב תל אביב 1": "maps/lev-tlv.webp",
    "פלורנטין 5": "maps/florentin.webp",
    "נווה שאנן 1": "maps/neve-shaanan.webp",
    "יד אליהו והתקווה 1": "maps/yad-eliyahu.webp",
    "שפירא 1": "maps/shapira.webp",
}
PANELS = {
    "נווה שרת טקסט 1": "panels/neve-sharet.webp",
    "נווה דן טקסט 1": "panels/neve-dan.webp",
    "רמת אביב טקסט 1": "panels/ramat-aviv.webp",
    "כוכב הצפוון טקסט 1": "panels/kochav-hatzafon.webp",
    "כוכב הצפון טקסט 1": "panels/kochav-hatzafon.webp",
    "הצפון הישן טקסט 1": "panels/old-north.webp",
    "לב תא טקסט 1": "panels/lev-tlv.webp",
    "פלורנטין טקסט 1": "panels/florentin.webp",
    "נווה שאנן טקסט 1": "panels/neve-shaanan.webp",
    "יד אליהו טקסט 1": "panels/yad-eliyahu.webp",
    "התקווה טקסט 1": "panels/hatikva.webp",
    "שפירא טקסט 1": "panels/shapira.webp",
    "קריית שלום טקסט 1": "panels/kiryat-shalom.webp",
}
COVER = {"כריכה סופית למחשב 1": "img/cover.webp"}
STICKER_PREFIXES = ("דמויות 8 2", "Property 1=Default", "Property 1=Variant2")

def norm(name):
    name = unicodedata.normalize("NFC", name)
    name = re.sub(r"\.(png|jpe?g|webp)$", "", name, flags=re.I)
    name = re.sub(r"@\d(\.\d+)?x", "", name)          # @2x
    name = re.sub(r"[-_ ]\d+$", "", name) if re.search(r"[-_]\d+$", name) else name  # Figma dup suffix "-1"
    return re.sub(r"\s+", " ", name).strip()

def save(img, rel, max_w, quality, lossless=False):
    out = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if img.width > max_w:
        img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
    img.save(out, "WEBP", quality=quality, method=6, lossless=lossless)
    print(f"  {rel:32s} {img.width}x{img.height}  {os.path.getsize(out)//1024} KB")
    return out

def main(src):
    files = [f for f in os.listdir(src) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    done, stickers = set(), []
    for f in sorted(files):
        key = norm(f)
        img = Image.open(os.path.join(src, f))
        if key in MAPS:
            # maps: 1728px is 1x; keep 2560 for sharp large screens
            save(img.convert("RGB"), MAPS[key], 2560, 80); done.add(MAPS[key])
        elif key in PANELS:
            save(img.convert("RGB"), PANELS[key], 820, 88); done.add(PANELS[key])
        elif key in COVER:
            c = img.convert("RGB")
            save(c, COVER[key], 2600, 80); done.add(COVER[key])
            og = c.copy(); og.thumbnail((1200, 1200))
            og.save(os.path.join(ASSETS, "img/og.jpg"), "JPEG", quality=82)
        elif key.startswith(STICKER_PREFIXES):
            stickers.append((f, img.convert("RGBA")))
        else:
            print(f"  (skipped, not recognised) {f}")
    # two sticker states: the darker one is the hover variant
    if stickers:
        def lum(im):
            small = im.resize((32, 32))
            px = [p for p in small.getdata() if p[3] > 128]
            return sum(0.3*r + 0.59*g + 0.11*b for r, g, b, a in px) / max(len(px), 1)
        stickers.sort(key=lambda t: lum(t[1]), reverse=True)
        save(stickers[0][1], "img/label.webp", 600, 90); done.add("img/label.webp")
        if len(stickers) > 1:
            save(stickers[-1][1], "img/label-hover.webp", 600, 90); done.add("img/label-hover.webp")
    expected = set(MAPS.values()) | set(PANELS.values()) | set(COVER.values()) | {"img/label.webp", "img/label-hover.webp"}
    missing = sorted(expected - done)
    print("\nMissing:" if missing else "\nAll assets in place.", *missing, sep="\n  ")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
