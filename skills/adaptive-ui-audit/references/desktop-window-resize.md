# Desktop · Window Resize & Min-Size (Area D1)

> Desktop apps are web-tech (React/Vue/Svelte/etc.) rendered inside a resizable native window (Electron `BrowserWindow`, Tauri window config). The user can drag the window to any size, span monitors of different DPR, and maximize on an ultra-wide. The web UI's responsive behavior is audited by the WEB analyzer (W1–W4); THIS area owns the *native window contract* around it: min-size bounds, resize behavior, fixed-size assumptions, multi-monitor/DPR scaling, and native chrome overlap. Scored area D1.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`.
Run this area ONLY if `PLATFORMS` includes `desktop` AND `FRAMEWORKS` (or the repo)
shows Electron or Tauri. If neither is present, emit nothing and record
"D1 skipped — no desktop shell detected". Confirm the shell before checking:

```bash
grep -rniE 'electron|@electron/|BrowserWindow' package.json 2>/dev/null | grep -v node_modules | head
find . -name 'tauri.conf.json' -not -path '*/node_modules/*' 2>/dev/null | head
grep -rniE '"@tauri-apps/' package.json 2>/dev/null | head
```

## Checks

### 1. Missing or absurd minimum window size (HIGH)
An Electron `BrowserWindow` created without `minWidth`/`minHeight` (or with a value so
small the layout collapses) lets the user drag the window below any breakpoint the web
UI was designed for — toolbars clip, sidebars overlap, content overflows. Tauri: the
window object in `tauri.conf.json` (`app.windows[]` in v2, `tauri.windows[]` in v1)
missing `minWidth`/`minHeight`.

```bash
# Electron: find window construction and inspect nearby min-size options
grep -rniE 'new BrowserWindow' --include='*.js' --include='*.ts' -n . 2>/dev/null | grep -v node_modules
grep -rniE 'minWidth|minHeight|useContentSize|resizable' --include='*.js' --include='*.ts' -n . 2>/dev/null | grep -v node_modules | head -40
# Tauri: window bounds in config
grep -rniE '"(minWidth|minHeight|width|height|resizable)"' $(find . -name 'tauri.conf.json' -not -path '*/node_modules/*') 2>/dev/null
```
A `BrowserWindow` with no `minWidth`/`minHeight` and a non-trivial layout → HIGH. Present
but very small (e.g. `minWidth < 640` for a dashboard-class app) → MEDIUM, confirm at runtime.

### 2. Layout breaks when the window shrinks (HIGH)
The classic desktop assumption: "it's a desktop app, nobody makes it small," so the web UI
ships with NO small-viewport breakpoints (cross-ref W2 Breakpoints). Dragging narrow then
produces whole-window horizontal scroll, clipped toolbars, or an unusable sidebar. Static
signal: min-size absent (Check 1) AND the CSS has no media/container queries below the
default desktop width.

```bash
grep -rncE '@media|@container|matchMedia|useWindowDimensions' src 2>/dev/null | grep -v ':0' | wc -l
grep -rniE 'width:\s*[0-9]{3,}px|min-width:\s*1[0-9]{3}px' --include='*.css' --include='*.scss' src 2>/dev/null | head
```
Tag: **W2/W1** (the defect is in the web UI; D1 owns only the missing native min-bound that
exposes it). Runtime-confirm by resizing to min bounds (see below).

### 3. Fixed size / `resizable:false` hiding a non-responsive layout (MEDIUM)
`resizable: false` or equal `width===minWidth===maxWidth` freezes the window so a
non-responsive layout never has to adapt. This is sometimes legitimate (a compact utility,
a login window) — flag the *assumption*, not always a defect. See `references/anti-patterns.md`
(fixed-size-is-fine): only escalate when the frozen size is large/primary and content is
clearly dynamic.

```bash
grep -rniE 'resizable\s*:\s*false|"resizable"\s*:\s*false|maximizable\s*:\s*false' -n . 2>/dev/null | grep -v node_modules | head
```
No dynamic content behind it → INFO. Primary window, dynamic/data-dense content frozen → MEDIUM.

### 4. Multi-monitor / DPR scaling & ultra-wide dead space (MEDIUM)
No `maxWidth` (or fluid max-width containers) means maximizing on a 3440px ultra-wide leaves
huge empty gutters or line-lengths >120ch (cross-ref W1 wasted space). DPR: hardcoded pixel
assets without `@2x`/`@3x` or `devicePixelRatio` handling blur on Retina/scaled monitors;
`window.screen`/`nativeTheme` reads that ignore per-display DPR when the window moves between
monitors.

```bash
grep -rniE 'devicePixelRatio|nativeImage|screen\.getPrimaryDisplay|getDisplayNearestPoint|@2x|@3x' -n . 2>/dev/null | grep -v node_modules | head
grep -rniE 'max-width|max-w-|container|clamp\(' --include='*.css' --include='*.tsx' src 2>/dev/null | head
```
Tag: **W1** for the web-side dead-space; D1 owns the native max-bound/DPR contract.

### 5. Native window chrome overlapping content (MEDIUM)
Frameless / custom title bars (`titleBarStyle: 'hidden'`/`hiddenInset`, `frame: false`,
`titleBarOverlay`, Tauri `decorations: false`) put OS controls (macOS traffic lights, Windows
caption buttons) on top of the web layout. Without a drag region and safe insets, the app's
own header buttons sit under the traffic lights and are unclickable, or content hides behind
the overlay.

```bash
grep -rniE "titleBarStyle|titleBarOverlay|frame\s*:\s*false|\"decorations\"|trafficLightPosition|-webkit-app-region" -n . 2>/dev/null | grep -v node_modules | head
```
Custom chrome with no reserved inset / `env(titlebar-area-*)` / `-webkit-app-region: drag` → MEDIUM.

## Runtime confirm (NO-INVENTED-OBSERVATIONS)
A visual break is OBSERVED only if a render confirms it; otherwise write
"Static analysis — confirm by <tool>". Per `references/runtime-validation.md`: launch the
built desktop app, then resize the native window (Playwright Electron `page.setViewportSize`
plus `BrowserWindow.setSize`, or the OS window manager) to (a) the configured min bounds — or
if none, 640×480 — and (b) an ultra-wide ~3440px, screenshotting each. Move the window across
two monitors of different DPR if available. Report each break as `screenshot@<WxH>`.

## SEVERITY / CONFIDENCE GUIDE
- CRITICAL: min-size absent AND runtime shows the primary window unusable (content clipped, controls unreachable) at a size the user can trivially reach.
- HIGH: no min-size on a dynamic primary window (Check 1/2), static-confirmed no small breakpoints.
- MEDIUM: fixed-size hiding non-responsive layout, ultra-wide dead space, chrome overlap — pending runtime.
- LOW/INFO: legitimate fixed utility window; cosmetic gutter at extreme widths.
- CONFIDENCE HIGH only with a screenshot at the offending size; static-only findings cap at MEDIUM confidence.

## SCORING HINTS
D1 base 100. Deduct CRITICAL −30 / HIGH −20 / MEDIUM −10 / LOW −4 / INFO 0, each ×confidence
(HIGH 1.0 / MED 0.75 / LOW 0.5); clamp 0–100. A missing min-size that runtime proves breaks the
primary window is the signature D1 CRITICAL. Do not double-count a web-UI breakpoint gap already
scored under W2 — tag it to W2 and let the report-generator dedup; D1 keeps only the native-contract deduction.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_d1_window_resize.md`. Each finding: check #, severity,
confidence, `file:line` (config or component), OBSERVED-vs-static marker (+ screenshot ref if
runtime), evidence, recommendation (the exact `minWidth`/`minHeight`/inset/max-width fix). Record
the detected shell (Electron/Tauri) and whether runtime resize was performed.
