# Troubleshooting capture runs

## App fails to load / load_timeout errors

The driver launches `app.R` in a fresh R process; anything that works interactively may fail there.

- Run the generated temp `app.R` standalone first (e.g., with `shiny::runApp()` from its directory) and fix startup errors before driving.
- Check the package entry point exists and is callable as written (internal functions need `pkg:::`).
- Make sure dev-only dependencies (`shinytest2`, `chromote`, `webshot2`, plus anything the app needs at runtime) are installed in the R library the driver uses.
- On slow machines or first run (browser download), raise `load_timeout` beyond 30000 ms.

## Blank, stale, or half-rendered screenshots

- The state did not finish rendering before capture: add a short wait (`Sys.sleep(0.3)`) after the interaction and before `get_screenshot()`, especially for charts, tables, and client-side JS.
- Verify by opening the PNG; a blank page usually means the app errored on load (check driver output/logs).
- If only part of the layout is visible, widen/tall the viewport at `AppDriver$new()` rather than scrolling.

## Clicks and set_inputs that do nothing

- `set_inputs()` uses Shiny **input names** (server-side argument names), not CSS selectors. A mismatched name is a silent no-op; confirm against the server function signature.
- `click(selector)` needs a stable selector: prefer explicit `id=` attributes on buttons/inputs over text-based matching, and `a[data-value='TabName']` for default Shiny tabs.
- If an element sits inside a tab that isn't active yet, click the tab first — hidden elements are not clickable.

## Leftover processes after a crashed run

A mid-run crash can leave orphaned R/chrome processes holding ports or temp files:

- Always call `app$stop()` on the normal path; if a run dies hard, kill stray chrome/R processes (Task Manager on Windows) before retrying.
- Temp app directories are unique per run (`tempfile()`), so stale ones do not collide — delete them manually if cleanup was skipped.

## Non-deterministic content in images

Timestamps, random sample IDs, or user-specific data make screenshots unreproducible and leak information. Seed temp state with fixed demo records (see `state_isolation.md`) and avoid time-driven UI in captured states where possible.
