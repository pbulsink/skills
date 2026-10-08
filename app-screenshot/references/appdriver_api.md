# shinytest2 AppDriver API notes

`shinytest2::AppDriver` drives a live Shiny app through a headless browser (chromote). Use it for scripted walkthroughs and screenshots.

## Creating a driver

```r
app <- shinytest2::AppDriver$new(
  app_dir,              # directory containing app.R (preferred) or a shiny.appobj
  name = "unique-name", # must be unique per concurrent run
  height = 900,         # viewport px; determines screenshot size
  width = 1300,
  load_timeout = 30000  # ms to wait for initial app load
)
```

Prefer pointing at a directory with a standalone `app.R` (see `state_isolation.md`) over an in-memory `shiny.appobj`: the file is where options can be set before the package loads.

Always call `app$stop()` when done, then remove the temp app directory.

## Core methods

| Method | Purpose |
|--------|---------|
| `app$get_screenshot(path)` | Save the current viewport as a PNG to `path`. |
| `app$set_inputs(input_id = value, ...)` | Set one or more Shiny inputs by input name; the app reacts before returning. Call repeatedly to fill a form step by step. |
| `app$click(selector)` | Click the first element matching a CSS selector (buttons, tabs, links). |
| `app$get_value(input_id)` | Read back an input's current value (useful for assertions and debugging). |
| `app$find_element(css)` | Locate one element by CSS selector; inspect or interact with it directly. |
| `app$stop()` | Stop the app and browser, release resources. |

## Selectors

- Inputs: use Shiny **input names** in `set_inputs()` — these are the server-side argument names. They usually match the UI `id=` but not always; confirm against the server function signature.
- Buttons/links: prefer explicit `id=` attributes on the UI (`actionButton("Label", "add_item")` -> `#add_item`). Avoid text-based selectors; labels change with i18n and refactors.
- Default Shiny tabs render as nav links carrying their tab name: `a[data-value='TabName']`.
- Any valid CSS selector works (chromote passes it to the browser).

## Waiting behavior

AppDriver waits for the app to become idle after each interaction, so reactive updates triggered by `set_inputs()`/`click()` are normally complete before the next call. Add explicit waits (`Sys.sleep(0.3)`) only for rendering Shiny does not track as activity — client-side JS, chart animations, heavy table renders — and immediately before a screenshot if the state looks half-drawn.

## Viewport

`height`/`width` fix the viewport (and thus every screenshot's size). Pick dimensions where the documented layout fits without horizontal scrollbars; 1300x900 is a sensible default for app tours.
