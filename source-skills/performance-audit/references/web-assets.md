# Web · Assets — Images, Fonts, CSS (Step W5, scored area, base 100)

> Evaluate media and style delivery: unoptimized/oversized images, missing dimensions (CLS), wrong lazy/eager choices, blocking/oversized fonts, huge/global CSS. Web scope only.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `platform=web`, `IMAGE_SOLUTION`, `STYLING`, `FRAMEWORKS`. Skip native apps.

## Images

### 1. Raw `<img>` bypassing the framework image optimizer (HIGH)
Next `<img>` instead of `next/image`, Astro `<img>` instead of `<Image>`, no
responsive `srcset`/`sizes`, no modern format (AVIF/WebP). Flag raw tags where an
optimizer exists.
```bash
grep -rniE '<img\s' . --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.astro' --include='*.html' -n 2>/dev/null | grep -v node_modules | head -20
grep -rniE '(next/image|astro:assets|@nuxt/image|unpic|@unpic)' . -l 2>/dev/null | grep -v node_modules | head
```

### 2. Missing width/height / aspect-ratio → CLS (HIGH)
`<img>`/background images with no intrinsic dimensions or `aspect-ratio`, causing
layout shift. Flag images without width/height.

### 3. Oversized / wrong-format source images (MEDIUM–HIGH, if inspectable)
Large raw assets in the repo (multi-hundred-KB PNG/JPG where WebP/AVIF fit),
serving full-res into small containers.
```bash
find . -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' \) \
  -size +300k 2>/dev/null | grep -vE 'node_modules|/\.git/' | head -20 || echo "No >300KB raster assets found in repo"
```

### 4. Wrong lazy/eager choice (MEDIUM)
Above-the-fold/LCP image lazy-loaded (delays LCP) OR every below-the-fold image
eager (wastes bandwidth). Flag `loading="lazy"` on the hero and its absence far below.

## Fonts

### 5. Blocking / undisciplined font loading (MEDIUM)
No `font-display: swap|optional`, fonts loaded render-blocking, no `preload` for
the critical font, or self-host vs third-party origin without `preconnect`.
```bash
grep -rniE '(font-display|@font-face|next/font|@fontsource|fonts.googleapis)' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.ts' --include='*.html' -n 2>/dev/null | grep -v node_modules | head
```

### 6. Excessive font families / weights / large files (LOW–MEDIUM)
Many families or many weights each shipping a full file; large unsubset fonts.
Flag > a couple of families or many weights with no subsetting.

## CSS

### 7. Huge / render-blocking / unnecessary global CSS (MEDIUM)
Large global stylesheets loaded on every route, unpurged utility CSS
(Tailwind without content purge), duplicated style systems (e.g. Tailwind +
styled-components + CSS modules together). Flag missing purge config.
```bash
grep -rniE '(content:\s*\[|purge:)' tailwind.config.* 2>/dev/null | head || echo "Check Tailwind content/purge config"
```

### 8. Expensive style/animation work (LOW)
Animating layout-triggering properties (width/height/top/left) instead of
transform/opacity; large numbers of expensive selectors. Flag only clear cases.

## SEVERITY GUIDE
- HIGH: LCP image not optimized/lazy-wrong, missing dimensions causing CLS.
- MEDIUM: font blocking, oversized images, unpurged/huge CSS.
- LOW/INFO: extra weights, minor selector cost.

## CONFIDENCE GUIDE
- HIGH: raw `<img>`/missing dimensions/blocking font directly in source.
- MEDIUM: image "too big for container" inferred without runtime layout data.
- LOW: CLS magnitude — needs Lighthouse/field data.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
LOW-confidence at half. Bonus: framework image optimizer used +5; `font-display`
+ preload discipline +5; purged CSS +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w5_assets.md`. Findings with app, severity,
confidence, `file:line`, and the confirming tool (Lighthouse, DevTools coverage,
image byte inspection). Per-severity count.
