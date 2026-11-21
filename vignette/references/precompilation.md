# Precompiling network-dependent and long-running vignettes

## When to use

Use this pattern when a vignette's examples need internet access (downloading
external data) or long-running computation, and the documentation engine —
`R CMD build`, `devtools::build_vignettes()`, CRAN checks, readers' RStudio —
must not execute that code. The pattern is used by scasanova/f1dataR in its
`vignettes/` directory and derives from Yihui Xie's ROpenSci post
"precompute vignettes" (https://ropensci.org/blog/2019-12-08/precompute-vignettes/).

## The two-file pattern

| File | Role |
|---|---|
| `vignettes/<name>.Rmd.orig` | Source of truth. Contains live code chunks. Author and edit **only** here. |
| `vignettes/<name>.Rmd` | Compiled static twin. Generated, committed, and what the documentation engine builds. Never hand-edit it. |

Why `.orig` works: R's vignette builder only recognizes sources with
extensions `.Rnw`, `.Rmd`, and `.Rwx`. A `.Rmd.orig` file ships in the source
tarball but is never built, so CRAN checkers and readers never execute
network or long-running code.

What compilation does — one live knit of the source:

- Runs every chunk once against real data/network.
- Chunks become inert ```` ``` r ```` fenced blocks; outputs are inlined as
  `#>` comments. The fences no longer carry knitr chunk headers, so the twin
  is pure content.
- Figures are written as `<fig.path prefix><chunk>-1.png` and referenced from
  the twin with raw HTML:
  `<div class="figure"><img src="..." ...></div>`, which passes through to
  `html_vignette` output untouched.
- `include = FALSE` setup chunks disappear entirely.

## Authoring a `.orig` file

The standard vignette rules in SKILL.md apply on top of these additions. The
setup chunk should follow this convention:

```{r setup, include = FALSE}
knitr::opts_chunk$set(
  collapse = TRUE, comment = "#>", out.width = "100%",
  fig.path = "<name>-",      # MUST equal the vignette base name; scripts locate figures by it
  dpi = 250, dev = "png"
)
knitr::knit_hooks$set(optipng = knitr::hook_optipng)  # if optipng is installed

# Point any package data cache at a temp dir so precompilation does not pollute
# the real user-facing cache:
withr::local_options(<pkg>.cache = file.path(tempdir(), "vignettes", "vig_build_tmp"))
withr::local_timezone("UTC")   # deterministic output for time-dependent code
```

The `fig.path` prefix must equal the vignette base name — both bundled scripts
rely on that convention to find and move generated figures.

Determinism tips (the compiled twin is a snapshot):

- Fix timezone/locale; use `set.seed()` for random data.
- Pin dataset versions where possible.
- State in the narrative when data was fetched (e.g., "data as of 2024-11"),
  because compiled outputs go stale if upstream data changes.

## Workflow

1. Author `vignettes/<name>.Rmd.orig`.
2. Copy `scripts/precompile_vignettes.R` from this skill into the package's
   `vignettes/` directory (once; commit it there).
3. From the package root run:
   `Rscript vignettes/precompile_vignettes.R --build`
4. Review the generated `.Rmd` twin and PNGs. If outputs are stale or ugly,
   fix the `.orig` file and re-run the compiler (it is idempotent).
5. Commit the `.orig`, the twin `.Rmd`, and all new/changed PNGs together.
6. Ensure `vignettes/.gitignore` contains:

   ```
   *.html
   *.R
   ```

## Maintenance rules

- Edited a `.orig`? Re-run the compiler before committing — the twin is a
  build artifact kept in git, and it must stay fresh.
- Never hand-edit a compiled `.Rmd`; fix the `.orig` and re-knit.
- Never commit figures from the package root; the compiler moves them into
  `vignettes/`.

## CRAN / size considerations

- All figures are committed PNGs. Compress with optipng at knit time (the
  `hook_optipng` hook) or afterwards (`xfun::optipng()`) to keep the tarball
  small; watch for CRAN's large-vignette warnings.
- The compiled output must be self-contained: no network calls, no long
  downloads. That is the whole point of the pattern.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Figures missing from twin | `fig.path` prefix does not equal the vignette base name, or figures were left in the package root. Run the compiler and checker scripts. |
| `knit()` cannot determine an engine | Pass both paths: `knitr::knit("vignettes/x.Rmd.orig", "vignettes/x.Rmd")` — knitr selects the engine from the **output** extension. |
| Outputs stale after data changes | Re-knit; consider noting the fetch date in the narrative. |
