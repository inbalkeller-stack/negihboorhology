# שכונולוגיה · Neighborhology

An illustrated book about Tel Aviv neighbourhoods by Inbal Keller.
Live at **https://inbalkeller-stack.github.io/negihboorhology/**

Plain HTML/CSS/JS, built from the Figma file
[שכונולוגיה](https://www.figma.com/design/G3kKYV2LbLeE2VB62zxJjF/).
Every push to `main` publishes the `site/` folder automatically (see `.github/workflows/pages.yml`).

```
site/                  the website
  index.html           home cover + about/credits popups
  <neighbourhood>/     8 map pages: neve-sharet, ramat-aviv, old-north, lev-tlv,
                       florentin, neve-shaanan, yad-eliyahu, shapira
  404.html
  assets/              css, js, img, maps, panels, fonts
build/
  generate.py          regenerates the HTML (label positions come from Figma)
  prepare_assets.py    turns the Figma PNG export into WebP in site/assets
```

## One-time setup
Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Updating the art
1. In Figma, export as **PNG @2x** into one folder: the 8 map images inside each neighbourhood frame,
   the 12 `… טקסט 1` stats panels, `כריכה סופית למחשב 1` (cover) and both states of the `דמויות 8 2` label.
2. `pip install pillow && python3 build/prepare_assets.py <that-folder>`
3. Commit and push.

## Font
The design uses **NextExitFOT** (commercial). With a web licence, put `NextExitFOT-Light.woff2`,
`-Regular.woff2` and `-Bold.woff2` in `site/assets/fonts/` and add the `url(...)` line noted at the top
of `site/assets/css/style.css`. Until then visitors see **Heebo**.

## Preview locally
```bash
cd site && python3 -m http.server 8000   # http://localhost:8000
```
