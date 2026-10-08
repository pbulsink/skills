---
name: app-screenshot
trigger: capture Shiny app screenshots
description: This skill should be used when capturing screenshots of R Shiny apps for documentation — vignettes, READMEs, and app tours. Covers driving a live app with shinytest2's AppDriver, isolating demo state from real data, and producing numbered PNGs ready to embed.
compatibility: Requires R plus the `shinytest2`, `chromote`, and `webshot2` packages (dev-only dependencies).
---

# App screenshots

Capture deterministic screenshots of a running Shiny app for documentation. Drive the live app with `shinytest2::AppDriver`, keep demo runs isolated from real data, and write numbered PNGs in user-journey order ready to embed in vignettes or READMEs.

## When to use
- Capture new screenshots for a Shiny app's vignette, README, or tour.
- Refresh existing screenshots after UI changes.
- Script a repeatable walkthrough of an app (fill inputs, click buttons, switch tabs) and record each state.

## Workflow
1. **Plan the shot list.** Decide every screenshot before running: filename, app state, and the interaction that reaches it. Order by user journey; zero-pad numbers so files sort in order. See `references/naming_embedding.md`.
2. **Isolate demo state.** Never let a capture run touch real data. Write a standalone `app.R` into a temp directory that points the app at temp state before starting it — `options()` set in this session do NOT reach the process shinytest2 launches. See `references/state_isolation.md`.
3. **Adapt the template.** Copy `scripts/capture_app_screenshots.R` into the target package and fill in every TODO: output directory, entry point, input names, selectors, shot list.
4. **Run it from the package root** with Rscript. Verify each PNG shows the intended state — blank or half-rendered images mean missing waits or a load failure; see `references/troubleshooting.md`.
5. **Embed in order.** Reference images by relative path from the document (`images/01_...png` inside vignettes, `vignettes/images/...` from a root README).

## Bundled scripts

| Script | Purpose |
|--------|---------|
| `scripts/capture_app_screenshots.R` | Parameterized template: copy into the target package and fill in every TODO before running. Not part of any package build. |

## Reference material
- `references/appdriver_api.md` — AppDriver methods, selectors, waiting behavior
- `references/state_isolation.md` — keeping capture runs away from real data
- `references/naming_embedding.md` — filename and embedding conventions
- `references/troubleshooting.md` — load failures, stale screenshots, selector problems

## Rules
- Re-run the capture script after any Shiny UI change; do not hand-edit committed screenshots.
- Use stable selectors: Shiny input names for `set_inputs()`, element `id=` attributes for clicks, `a[data-value='TabName']` for default Shiny tabs.
- Add short waits only where rendering is client-side (charts, tables); AppDriver already waits for the app to settle after each interaction.
- Keep `shinytest2`, `chromote`, and `webshot2` out of `Imports`; they are dev-only (`Suggests`) dependencies used by this script alone.
