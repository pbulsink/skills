# State isolation patterns

Capture runs must never mutate real user data — local registries, databases, config files. A screenshot script that writes to production state is a bug even if the images look right.

## The callr gotcha

`shinytest2::AppDriver` launches the app in a **separate background R process** (via `callr`). That process does NOT inherit `options()` set in the driver session:

```r
# Does NOT reach the launched app -- do not rely on this
options(mypkg.state_path = "C:/temp/demo.db")
app <- shinytest2::AppDriver$new(app_dir)
```

Isolation must therefore happen inside the code that starts the app.

## Standalone app.R pattern

Write a tiny `app.R` into a temp directory that sets up isolated state and then starts the real app, and point AppDriver at that directory:

```r
demo_dir <- tempfile("app-tour-")
dir.create(demo_dir)
demo_db <- file.path(demo_dir, "demo.db")   # empty/temp state file

writeLines(
  sprintf(
    paste0(
      "options(mypkg.state_path = %s)\n",          # app-specific option for its data path
      "pkgload::load_all(%s, quiet = TRUE)\n",     # library(pkg) if installed instead
      "mypkg::run_app()\n"                          # entry point that starts the Shiny app
    ),
    deparse(demo_db),
    deparse(normalizePath("."))
  ),
  file.path(demo_dir, "app.R")
)

app <- shinytest2::AppDriver$new(demo_dir, name = "app-tour")
# ... capture screenshots ...
app$stop()
unlink(demo_dir, recursive = TRUE)
```

Notes:
- The `options()` call must run **before** the package loads/starts if the app reads its option at startup.
- Use a unique driver `name` per target so concurrent runs don't collide.
- Clean up the temp directory after `app$stop()`.

## If the app has no path option

- Prefer an entry point that accepts a state/path argument and call it with a temp value from inside `app.R`.
- Otherwise redirect via environment variable if the app honors one (set it in `app.R` before starting).
- If neither exists, do not run captures against real state: add such an option to the app first (dev-only) or capture only read-only views.

## Demo data

Seed temp state with small, fixed demo records so screenshots are deterministic — no timestamps, random IDs, or user-specific content in committed images.
