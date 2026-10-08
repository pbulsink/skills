# Template for capturing screenshots of a Shiny app for documentation.
# Not part of any package build -- copy this file into the target package and
# fill in every TODO before running. Re-run after any Shiny UI change to
# refresh the images.
#
# Requires: shinytest2, chromote, webshot2 (Suggests-only, dev use)
#
# IMPORTANT: shinytest2::AppDriver launches the app in a separate background
# R process (via callr), which does NOT inherit options() set in this session.
# Demo state is therefore isolated inside a tiny standalone app.R written into
# a temp directory below -- not via options() here.

img_dir <- file.path("vignettes", "images")  # TODO: where screenshots are written
dir.create(img_dir, showWarnings = FALSE, recursive = TRUE)

demo_dir <- tempfile("app-tour-")
dir.create(demo_dir)

# TODO: temp state files the app needs (e.g. an empty SQLite DB seeded with demo records)
demo_state <- file.path(demo_dir, "demo.db")

pkg_root <- normalizePath(".")  # TODO: package root if not running from it
writeLines(
  sprintf(
    paste0(
      "# Runs inside the launched app process -- isolation happens here\n",
      "options(mypkg.state_path = %s)\n",   # TODO: option that redirects the app's data path
      "pkgload::load_all(%s, quiet = TRUE)   # library(pkg) if the package is installed\n",
      "mypkg::run_app()                      # TODO: entry point that starts the Shiny app\n"
    ),
    deparse(demo_state),
    deparse(pkg_root)
  ),
  file.path(demo_dir, "app.R")
)

app <- shinytest2::AppDriver$new(
  demo_dir,
  name = "app-tour",        # TODO: unique per target app / concurrent run
  height = 900,             # TODO: viewport size matching the documented layout
  width = 1300,
  load_timeout = 30000
)

snap <- function(filename) {
  app$get_screenshot(file.path(img_dir, filename))
}

# --- Shot list -----------------------------------------------------------------
# TODO: replace with the target app's journey. One numbered block per screenshot,
# in user-journey order; zero-padded filenames sort correctly.

# --- 1. Landing view: nothing entered yet ---------------------------------------
Sys.sleep(0.5)
snap("01_landing.png")

# --- 2. Navigate to a tab --------------------------------------------------------
app$click(selector = "a[data-value='TabName']")  # TODO: stable selector for the tab
Sys.sleep(0.3)
snap("02_tab_name.png")

# --- 3. Fill inputs and submit ----------------------------------------------------
app$set_inputs(input_id_1 = "value")             # TODO: real input names/values
app$set_inputs(input_id_2 = "value")
app$click(selector = "#submit_button")           # TODO: stable selector for the action
Sys.sleep(0.3)
snap("03_result.png")

app$stop()
unlink(demo_dir, recursive = TRUE)

message("Screenshots written to ", normalizePath(img_dir))
