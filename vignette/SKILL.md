---
name: vignette
trigger: create vignettes
description: This skill should be used when creating or updating package vignettes. Vignettes are workflow-focused guides for users familiar with R but new to the package.
compatibility: Requires R and the `usethis` package.
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

Avoid internet access when possible.

Prefer plots over tables.

Mention internal functions only when essential.

### Validation

Verify:
- File is in `vignettes/`.
- Extension is `.Rmd`.
- Filename and title follow conventions.
- First chunk is setup.
- Chunk names are unique.
- Vignette builds successfully (creates [vignette_name].html file)
- Narrative focuses on workflows.
- Realistic package usage is demonstrated.

Repeat verification of content on generated html file.
