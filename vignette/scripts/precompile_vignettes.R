#!/usr/bin/env Rscript
# precompile_vignettes.R
#
# Compile long-running / network-dependent vignette sources into static twins.
#
# Each source `vignettes/<name>.Rmd.orig` is knitted once with a live session;
# the result is written to `vignettes/<name>.Rmd`, where code chunks become
# inert fenced blocks with inlined outputs and figures are referenced as PNGs.
# The normal documentation engine (R CMD build, devtools::build_vignettes)
# only ever sees the static twin, so readers and CRAN checks never execute
# network or long-running code.
#
# Usage (from the package root):
#   Rscript vignettes/precompile_vignettes.R [--build] [--skip-compress]
#
#   --build         Run devtools::build_vignettes() afterwards to verify the
#                   static twins build cleanly (requires devtools).
#   --skip-compress Skip post-hoc xfun::optipng() compression of PNG figures.
#
# Conventions this script relies on:
#   * The setup chunk of every .orig file sets fig.path to "<name>-" where
#     <name> is the vignette base name (figures are located by that prefix).
#   * knitr::knit() picks the knit engine from the OUTPUT extension, so
#     knitting a ".Rmd.orig" input into a ".Rmd" output works as-is.

args <- commandArgs(trailingOnly = TRUE)
do_build        <- "--build" %in% args
skip_compress   <- "--skip-compress" %in% args

pkg_root      <- getwd()
vignettes_dir <- file.path(pkg_root, "vignettes")
stopifnot(dir.exists(vignettes_dir))

orig_files <- list.files(vignettes_dir, pattern = "\\.Rmd\\.orig$")
if (length(orig_files) == 0L) {
  message("No .Rmd.orig files found in ", vignettes_dir, ". Nothing to do.")
  quit(save = "no", status = 0L)
}

for (orig in orig_files) {
  target <- sub("\\.orig$", "", orig)
  prefix <- sub("\\.Rmd\\.orig$", "", orig)

  message("Compiling ", vignettes_dir, "/", orig, " -> ", target)
  knitr::knit(file.path(vignettes_dir, orig), file.path(vignettes_dir, target))

  # fig.path is resolved relative to the working directory (package root), so
  # generated figures land in pkg_root and must be moved into vignettes/.
  candidates <- list.files(pkg_root, pattern = "\\.(png|svg)$")
  figs <- candidates[startsWith(candidates, paste0(prefix, "-"))]
  for (fig in figs) {
    file.copy(file.path(pkg_root, fig), file.path(vignettes_dir, fig), overwrite = TRUE)
    unlink(file.path(pkg_root, fig))
    message("Moved figure ", fig, " -> vignettes/")
  }
}

if (!skip_compress && requireNamespace("xfun", quietly = TRUE)) {
  message("Compressing PNG figures with xfun::optipng()")
  invisible(xfun::optipng(vignettes_dir, verbose = FALSE))
} else if (skip_compress) {
  message("Skipping figure compression (--skip-compress)")
}

if (do_build) {
  if (!requireNamespace("devtools", quietly = TRUE)) {
    stop("--build requires the devtools package")
  }
  message("Running devtools::build_vignettes() to verify static twins")
  devtools::build_vignettes()
}

message("Done. Review the generated .Rmd files and figures, then commit both.")
