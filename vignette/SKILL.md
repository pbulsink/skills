---
name: vignette
trigger: create vignettes
description: This skill should be used when creating or updating package vignettes. Vignettes are workflow-focused guides for users familiar with R but new to the package.
compatibility: Requires R with `usethis` and `knitr`; optionally
  `xfun` (figure compression) and `devtools` (verification builds) for
  precompiled vignettes.
---

## Package vignettes

Write workflow-focused vignettes for users familiar with R but unfamiliar with
the package. Style should resemble a technical blog post, not reference
documentation. Vignettes support both learning and SEO.

### Goals

Demonstrate:
- Typical workflows.
- Unique package features.
- Interesting datasets.
- Challenging or edge-case scenarios.

Show how users solve problems with the package, not how individual functions
work.

### File creation

Vignettes must be `.Rmd` files in `vignettes/`.

Create with:

```r
usethis::use_vignette(filename, title)
```

Rules:
- filename: lowercase_with_underscores
- title: Title Case

### Content

Structure:
1. Introduction/problem
2. Setup
3. Workflow
4. Results/discussion
5. Summary

First chunk must be a named setup chunk containing configuration only.

All chunks:
- Must be named.
- Must be preceded by explanation.
- Must be followed by interpretation.
- Explanations should provide reasoning, not restate code.
- Interpretations should explain implications, not restate output.

Target roughly:
- 60% narrative
- 40% code

### Data and examples

Prefer:
1. Package datasets
2. Base R datasets
3. Datasets from imported/suggested packages
4. Synthetic data

Avoid internet access when possible. When a workflow genuinely requires
internet access or long-running computation, use the precompiled-vignette
pattern below instead of removing the example.

Prefer plots over tables.

Mention internal functions only when essential.

### Precompiling network- or long-running vignettes

When a vignette needs internet access or long-running computation, keep the
documentation engine (and CRAN checks) away from that code using a two-file
pattern:

- Author in `vignettes/<name>.Rmd.orig` — the source of truth with live chunks.
- Compile it once into `vignettes/<name>.Rmd`, a static twin with inert code
  fences, inlined outputs, and committed PNG figures. The documentation engine
  only ever builds the twin; `.orig` files are never built by R.

Workflow:
1. Write the `.orig` file per the content rules above; its setup chunk must set
   `fig.path = "<name>-"` (equal to the vignette base name).
2. Copy `scripts/precompile_vignettes.R` from this skill into the package's
   `vignettes/` directory, then run from the package root:
   `Rscript vignettes/precompile_vignettes.R --build`
3. Review the generated twin and figures; re-run after any `.orig` edit.
4. Commit the `.orig`, the twin `.Rmd`, and all PNGs together; keep
   `vignettes/.gitignore` containing `*.html` and `*.R`.
5. Validate with `scripts/check_precompiled_vignettes.R` (exits non-zero on
   missing twins, live chunks in a twin, or broken figure references).

Never hand-edit a compiled `.Rmd` — fix the `.orig` and recompile. See
`references/precompilation.md` for setup-chunk conventions, determinism tips,
maintenance rules, and CRAN size considerations.

### Validation

Verify:
- File is in `vignettes/`.
- Extension is `.Rmd`.
- Filename and title follow conventions.
- First chunk is setup.
- Chunk names are unique.
- Vignette builds successfully (creates [vignette_name].html file)
- For precompiled vignettes: the `.Rmd` twin exists, contains no live chunks,
  and every figure reference resolves to a committed PNG in `vignettes/`
  (`scripts/check_precompiled_vignettes.R` automates these checks)
- Narrative focuses on workflows.
- Realistic package usage is demonstrated.

Repeat verification of content on generated html file.
