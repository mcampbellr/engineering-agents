# Project Discovery & Scope (Step 0)

> Profile the project and determine platform scope (web / native / desktop / combos) BEFORE any analysis. Framework-agnostic, monorepo-aware, responsive-system-aware. This is the MANDATORY first step; if no user-facing UI exists, the audit stops here. Never assume the stack — detect it from evidence.

---

Goal: Produce the discovery artifact all downstream steps depend on. Record
platform per app, framework & rendering, the responsive/styling system and its
breakpoints, viewport meta, safe-area & keyboard handling, orientation config,
large-screen navigation, UI libs, and available runtime tooling. If no UI runtime
is detected, report cleanly and stop.

## PROJECT ROOT, APPS & PATHS (execute first)

- Identify manifests: `package.json`, `pubspec.yaml` (Flutter), `app.json` /
  `app.config.{js,ts}` (Expo), `src-tauri/tauri.conf.json` (Tauri).
- **Monorepo detection:** look for `pnpm-workspace.yaml`, `turbo.json`, `nx.json`,
  `lerna.json`, `rush.json`, or a `workspaces` field in root `package.json`. If
  present, enumerate every app under `apps/*`, `packages/*`, and workspace globs.
  Record each as a separate `APP` with its own platform/framework. Shared
  `packages/*` are audited once as shared UI code.

```bash
ls pnpm-workspace.yaml turbo.json nx.json lerna.json 2>/dev/null
find . -maxdepth 4 -name package.json 2>/dev/null | grep -vE 'node_modules|/dist/|/build/' | head -40
find . -maxdepth 3 \( -name 'app.json' -o -name 'app.config.*' -o -name 'pubspec.yaml' -o -name 'tauri.conf.json' \) 2>/dev/null | grep -v node_modules
```

## PLATFORM DETECTION (web vs native vs desktop)

Classify EACH app. Do not mix rules across platforms.

```bash
# Native / mobile signals
grep -rniE '"(react-native|expo|expo-router|@react-navigation/[a-z-]+|nativewind|react-native-reanimated)"' package.json 2>/dev/null && echo "NATIVE:react-native/expo"
test -f pubspec.yaml && grep -qiE '^\s*flutter\s*:' pubspec.yaml && echo "NATIVE:flutter"

# Desktop signals (web-tech in a resizable native window)
grep -rniE '"(electron|electron-builder|@electron/[a-z-]+)"' package.json 2>/dev/null && echo "DESKTOP:electron"
{ test -d src-tauri || grep -rqiE '"@tauri-apps/' package.json 2>/dev/null; } && echo "DESKTOP:tauri"

# Web framework signals
grep -rniE '"(next|nuxt|@remix-run/[a-z-]+|astro|@sveltejs/kit|svelte|@angular/core|vue|react-dom|vite|gatsby)"' package.json 2>/dev/null && echo "WEB:framework"
```

Resolve platform per app:
- **native** — `react-native`/`expo` present, or Flutter (`pubspec.yaml` with a
  `flutter:` block). Note Expo vs bare RN, Expo SDK version.
- **desktop** — Electron (`electron` dep + a main-process entry, e.g. `main.js`
  / `electron.js` / `background.js`) or Tauri (`src-tauri/` or `@tauri-apps/*`).
  Desktop apps render web tech → they run the WEB checks PLUS the D1 window-resize
  area. Identify the renderer's web framework too.
- **web** — a web framework or `react-dom`/DOM bundling present, no RN/desktop.
- A monorepo may contain several → project `PLATFORMS` is the SET (e.g.
  `web,native`); each app keeps its own.

## FRAMEWORK / RENDERING STRATEGY

Identify framework and rendering from config + code, not guesses:
- **Next.js** — `next.config.*`; App Router (`app/`) vs Pages; `output: 'export'`.
- **Astro** — `astro.config.*`; client directives.
- **Nuxt / Vue** — `nuxt.config.*`; `ssr: true|false`.
- **SvelteKit / Svelte** — `svelte.config.*`; adapter.
- **Remix / Angular / Vite / vanilla** — respective configs.
- **Expo / RN** — Expo Router vs React Navigation; New Architecture.
- **Flutter** — widget-tree signals; `MediaQuery` / `LayoutBuilder` usage.

## RESPONSIVE / STYLING SYSTEM (drives every layout check)

Detect the styling system AND where breakpoints are defined:

```bash
# Styling system
grep -rniE '"(tailwindcss|nativewind|styled-components|@emotion/[a-z-]+|@vanilla-extract/[a-z-]+|@stitches/react|classnames)"' package.json 2>/dev/null | head
ls tailwind.config.* 2>/dev/null && grep -nE 'screens' tailwind.config.* 2>/dev/null
# CSS Modules / raw CSS media & container queries
grep -rlnE '@media|@container|container-type' . --include='*.css' --include='*.scss' --include='*.module.css' 2>/dev/null | grep -v node_modules | head
# Flutter responsive primitives
grep -rlnE 'MediaQuery|LayoutBuilder|OrientationBuilder' . --include='*.dart' 2>/dev/null | head
```

Record `RESPONSIVE_SYSTEM` (tailwind / nativewind / css-modules / styled-components /
emotion / vanilla-extract / stitches / raw-css / flutter-mediaquery / inline) and
`BREAKPOINTS` (the actual source — Tailwind `screens`, a `@media` list, a
breakpoints constant, or "none found").

## VIEWPORT META (web/desktop only)

```bash
grep -rnE '<meta[^>]+name=["'\'']viewport' . --include='*.html' --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.astro' 2>/dev/null | grep -v node_modules | head
# Next.js metadata / expo web
grep -rnE 'viewport\s*[:=]|generateViewport|initialScale|maximum-scale|user-scalable' . --include='*.ts' --include='*.tsx' 2>/dev/null | grep -v node_modules | head
```
Record `VIEWPORT_META` (present-correct / present-with-maximum-scale-lock /
missing / n-a-native). A `maximum-scale=1` or `user-scalable=no` blocks zoom → note
it for W4.

## SAFE AREA, KEYBOARD, ORIENTATION (native)

```bash
# Safe area
grep -rniE '"(react-native-safe-area-context|react-native-safe-area-view)"' package.json 2>/dev/null
grep -rnE 'env\(safe-area-inset-|SafeAreaView|useSafeAreaInsets|SafeArea\(' . --include='*.tsx' --include='*.ts' --include='*.dart' --include='*.css' 2>/dev/null | grep -v node_modules | head
# Keyboard handling
grep -rniE '"(react-native-keyboard-controller|react-native-keyboard-aware-scroll-view)"' package.json 2>/dev/null
grep -rnE 'KeyboardAvoidingView|resizeToAvoidBottomInset|keyboardShouldPersistTaps' . --include='*.tsx' --include='*.ts' --include='*.dart' 2>/dev/null | grep -v node_modules | head
# Orientation config
grep -rnE '"orientation"|orientation:|screenOrientation|UISupportedInterfaceOrientations' app.json app.config.* android/app/src/main/AndroidManifest.xml ios/*/Info.plist 2>/dev/null | head
```
Record `SAFE_AREA` (safe-area-context / expo / env-inset / flutter-safearea / none),
`KEYBOARD_HANDLING` (keyboard-controller / kbd-aware-scroll / KeyboardAvoidingView /
resizeToAvoidBottomInset / none), `ORIENTATION` (locked-portrait / locked-landscape /
sensor / unspecified).

## NAVIGATION & LARGE-SCREEN LAYOUTS

Detect whether tablet/desktop layouts exist at all (a common gap):
```bash
grep -rnE 'isTablet|useMediaQuery|useWindowDimensions|Dimensions\.get|min-width|lg:|xl:|2xl:|MediaQuery\.of|breakpoint' . \
  --include='*.tsx' --include='*.ts' --include='*.dart' --include='*.css' 2>/dev/null | grep -v node_modules | head -20
```
Record `NAV_LARGE_SCREEN` (has-tablet-desktop-layouts / mobile-only / desktop-only /
unknown). Also note the UI/design-system libs (MUI, Chakra, Ant, Mantine, shadcn/ui,
Tamagui, React Native Paper, Flutter Material/Cupertino) — they carry their own
responsive primitives.

## RUNTIME TOOLING CAPABILITY (detect presence only — install nothing)

Record what could drive an optional runtime render. See
`references/runtime-validation.md`.
```bash
# Dev/preview server scripts (do NOT assume a port — read it later)
grep -nE '"(dev|start|preview|serve)"\s*:' package.json 2>/dev/null | head
# Playwright / browser automation
grep -rniE '"(@playwright/test|playwright|puppeteer|cypress)"' package.json 2>/dev/null | head
# Native simulators/emulators (local availability)
xcrun simctl list devices available 2>/dev/null | grep -iE 'iphone|ipad' | head -3
which emulator adb 2>/dev/null
```
Also note the **claude-in-chrome browser MCP** as an available runtime driver when
present in the session. Record `RUNTIME_TOOLS` (comma list: dev-server-script,
playwright, claude-in-chrome, ios-simulator, android-emulator, or "none available").

## DECISION

- If NO web, native, or desktop UI app is detected (pure backend / library / CLI):
  set `PLATFORMS=none`. Write the artifact, then STOP and report: "No web, native,
  or desktop UI detected — adaptive-ui-audit targets user-facing layouts; nothing
  to audit here."
- Otherwise set `PLATFORMS` to the detected set (`web` | `native` | `desktop` |
  combos) and continue with the matching branch(es). Desktop implies the WEB
  branch + D1.

## ARTIFACT SAVE (mandatory)

Save to `reports/.artifacts/step_00_aui_discovery.md`. Run first:
`mkdir -p reports/.artifacts`

Output format (downstream steps parse these keys):
```
PLATFORMS=[web|native|desktop|comma-set|none]
RESPONSIVE_SYSTEM=[..]
BREAKPOINTS=[source + values, or "none found"]
VIEWPORT_META=[present-correct|present-scale-locked|missing|n-a-native]
SAFE_AREA=[..]
KEYBOARD_HANDLING=[..]
ORIENTATION=[..]
NAV_LARGE_SCREEN=[has-tablet-desktop|mobile-only|desktop-only|unknown]
RUNTIME_TOOLS=[comma list or "none available"]
APPS:
- name@path — platform=[web|native|desktop] framework=[..] rendering=[..]
...
SHARED_PACKAGES:
- name@path — [what UI it provides]
```
Followed by a short prose summary of the project and the scope decision (which
branches will run, per app).
