#!/usr/bin/env Rscript
# check_precompiled_vignettes.R
#
# Validate the precompiled-vignette setup of a package. Suitable for CI:
# exits with status 1 if any check fails, 0 otherwise.
#
# Usage (from the package root):
#   Rscript vignettes/check_precompiled_vignettes.R
#
# Checks (failures):
#   1. Every vignettes/<name>.Rmd.orig has a compiled <name>.Rmd twin.
#   2. Compiled twins contain no live knitr chunks (``` {r ...} headers).
#   3. Every <img src="..."> reference in a twin resolves to a file in
#      vignettes/ (catches figures left behind in the package root).
# Warnings only:
#   * A .orig file sets no fig.path option (the compiler locates figures by
#     the "<name>-" prefix convention).
#   * vignettes/.gitignore is missing.

vignettes_dir <- file.path(getwd(), "vignettes")
stopifnot(dir.exists(vignettes_dir))

failures  <- character()
warnings_ <- character()

orig_files <- list.files(vignettes_dir, pattern = "\\.Rmd\\.orig$")
twin_files <- setdiff(
  list.files(vignettes_dir, pattern = "\\.(Rnw|Rmd)$"),
  paste0(orig_files, ".orig")
)

for (orig in orig_files) {
  twin <- sub("\\.orig$", "", orig)
  if (!file.exists(file.path(vignettes_dir, twin))) {
    failures <- c(failures, sprintf("Missing compiled twin: vignettes/%s", twin))
    next
  }

  text <- paste(readLines(file.path(vignettes_dir, twin), warn = FALSE), collapse = "\n")

  # Live chunk headers look like ```{r name, ...} — compiled output uses inert
  # ``` r fences only. (?m) is required so ^ matches every line.
  if (grepl("(?m)^\\s*```\\{r", text, perl = TRUE)) {
    failures <- c(failures, sprintf("Compiled twin still contains live chunks: vignettes/%s", twin))
  }

  # Extract <img src="..."> references and verify each resolves locally.
  tags <- unlist(regmatches(text, gregexpr("<img[^>]*>", text)))
  for (tag in tags) {
    m <- regmatches(tag, regexec('src="([^"]+)"', tag))[[1]]
    if (length(m) != 2L) next
    ref <- m[2]
    if (!file.exists(file.path(vignettes_dir, ref))) {
      failures <- c(failures, sprintf("Broken figure reference in vignettes/%s: %s", twin, ref))
    }
  }

  orig_text <- paste(readLines(file.path(vignettes_dir, orig), warn = FALSE), collapse = "\n")
  if (!grepl("fig\\.path", orig_text)) {
    warnings_ <- c(warnings_, sprintf("No fig.path option found in vignettes/%s", orig))
  }
}

if (!file.exists(file.path(vignettes_dir, ".gitignore"))) {
  warnings_ <- c(
    warnings_,
    "vignettes/.gitignore is missing (expected entries: *.html and *.R)"
  )
}

for (w in warnings_) message("WARNING: ", w)
for (f in failures)  message("FAILURE: ", f)

if (length(failures) > 0L) {
  message(length(failures), " failure(s) found. Re-run the compiler after editing .orig sources.")
  quit(save = "no", status = 1L)
}
message("Precompiled vignette checks passed.", ifelse(length(orig_files) == 0L, " (no .orig files present)", ""))
