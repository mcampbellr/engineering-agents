# Runtime Validation — the Hybrid Heart

> Adaptive-UI defects are ultimately VISUAL. Static analysis finds the *suspects*; only a real render CONFIRMS them. This reference explains how to drive an optional runtime pass and, critically, defines the evidence rule: without a render, every visual claim stays "Static — confirm at <viewport/orientation>" and must name the tool that would confirm it. NEVER install tooling. NEVER assume a port — read it. The runtime pass is OPTIONAL and folded into the analyzers; the audit is fully valid as static analysis alone.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`
for `PLATFORMS`, `RESPONSIVE_SYSTEM`, `VIEWPORT_META`, `RUNTIME_TOOLS`.

## When a runtime pass is possible

- **WEB / DESKTOP-web** — possible when a dev/preview server can be started (a
  `dev`/`start`/`preview`/`serve` script exists) AND a driver is present:
  the **claude-in-chrome browser MCP** tools or **Playwright**. Detect the script;
  start it only if the user has authorized running the app, then read the actual
  URL/port from its output — never guess `localhost:3000`.
- **NATIVE** — you generally CANNOT auto-drive a simulator/emulator from here.
  Describe the assisted matrix and let a human (or the user's simulator) render;
  do not claim native renders you did not perform.

## WEB / DESKTOP recipe (claude-in-chrome MCP or Playwright)

Load the browser MCP tools via ToolSearch first if deferred. For each in-scope
route, run the viewport matrix and measure:

- **Viewport matrix**: 320, 360, 390, 768, 1024, 1280, 1440 (add 1920 for desktop
  windows). Use `resize_window` (MCP) or `page.setViewportSize` (Playwright).
- **Horizontal overflow**: `document.documentElement.scrollWidth > clientWidth`.
- **Oversized elements**: any element whose `getBoundingClientRect().right >
  window.innerWidth` (the culprit behind overflow).
- **Wasted space at wide widths**: measure the main content's rendered width vs
  `innerWidth` — a large empty gutter (e.g. content capped ~600px inside a 1440px
  window with no intentional `max-width` design) is a MEDIUM wasted-space finding.
- **Viewport meta effect**: confirm the page is not rendered zoomed-out (a missing
  `<meta viewport>` makes `innerWidth` ≫ CSS layout width).
- **Text zoom / reflow**: bump zoom to 200% (`document.body.style.zoom` or the
  browser zoom, or a root `font-size` increase) and re-scan for overflow / clipped
  / cut-off text and loss of reflow (content should reflow, not require horizontal
  scroll — WCAG 1.4.10).
- **Touch targets**: collect interactive elements (`a, button, [role=button],
  input, select, [onclick]`) whose bounding box is `< 44×44` CSS px.
- **Keyboard/input out of view (web forms)**: focus each input and check it is
  still within the visible viewport after any scroll.

Screenshots (`computer` / `page.screenshot`) are the evidence artifact — save them
under `reports/.artifacts/renders/` and cite the path in the finding.

### Copy-pasteable scan (overflow + oversized elements + small tap targets)

Run via `javascript_tool` (MCP) or `page.evaluate` (Playwright) at each viewport:

```js
(() => {
  const de = document.documentElement;
  const vw = window.innerWidth, vh = window.innerHeight;
  const overflowX = de.scrollWidth > de.clientWidth;
  const oversized = [...document.querySelectorAll('*')]
    .filter(el => { const r = el.getBoundingClientRect();
      return r.width > 0 && (r.right > vw + 1 || r.left < -1); })
    .slice(0, 20)
    .map(el => ({ tag: el.tagName.toLowerCase(),
      cls: (el.className && el.className.toString().slice(0, 60)) || '',
      right: Math.round(el.getBoundingClientRect().right) }));
  const smallTargets = [...document.querySelectorAll('a,button,[role=button],input,select,[onclick]')]
    .map(el => ({ el, r: el.getBoundingClientRect() }))
    .filter(({ r }) => r.width > 0 && (r.width < 44 || r.height < 44))
    .slice(0, 20)
    .map(({ el, r }) => ({ tag: el.tagName.toLowerCase(),
      w: Math.round(r.width), h: Math.round(r.height),
      txt: (el.textContent || '').trim().slice(0, 30) }));
  return { vw, vh, scrollWidth: de.scrollWidth, clientWidth: de.clientWidth,
    overflowX, oversized, smallTargets };
})();
```

`overflowX:true` with a non-empty `oversized` list is a HIGH-confidence OBSERVED
overflow finding, with the offending element named.

## NATIVE recipe (assisted / manual matrix)

You cannot auto-drive here — describe what to render and on what, and mark such
findings HIGH only if the user confirms the render. Matrix:

- **Devices**: small phone (e.g. iPhone SE), large phone (Pro Max / large Android),
  7" tablet, 10" tablet. **Orientation**: portrait AND landscape for each.
- **What to look at**:
  - Safe area — status bar, notch/Dynamic Island, and home-indicator not colliding
    with content or nav; insets applied on the right edges (iOS Simulator, Android
    emulator with a notch skin).
  - Keyboard over input — focus each text field on a small phone; the focused input
    must stay visible above the keyboard (device keyboard, not the hardware one).
  - Tablet wasted space — a phone layout stretched full-width on a 10" tablet is a
    wasted-space finding.
  - Text scaling — set OS font size / Dynamic Type to max (`fontScale` at max) and
    check for clipped or truncated text and broken layouts.
- **Tools to name**: iOS Simulator, Android emulator, Expo (device/simulator),
  device Settings → Display → Text Size / Accessibility → Larger Text.

## Evidence artifact convention (OBSERVED blocks)

An analyzer that performs a render appends an **OBSERVED** evidence block to its
own step artifact and marks those findings **confidence HIGH**:

```
### OBSERVED — <area/finding id>
- viewport/device: 390×844 (or "iPhone 15, portrait")
- route: /checkout
- tool: claude-in-chrome (resize_window + javascript_tool)
- measured: scrollWidth=520 > clientWidth=390 → horizontal overflow
- offending element: <table class="orders"> right=520
- screenshot: reports/.artifacts/renders/checkout_390.png
```

**Hard rule:** only a finding backed by an OBSERVED block may assert a pixel,
viewport, or visual fact as observed. Every other visual claim reads "Static
analysis — render at <viewport/orientation> with <tool> to confirm" and stays at
MEDIUM/LOW confidence. If no runtime pass ran at all, the report's score is
labeled a **static readiness signal** (see SKILL.md scoring).
