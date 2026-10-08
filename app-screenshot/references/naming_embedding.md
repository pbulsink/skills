# Screenshot naming and embedding conventions

## Filenames

- Zero-padded numeric prefix + snake_case description: `01_landing.png`, `02_viscometers_tab_empty.png`.
- Zero-padding (two digits) keeps lexicographic order equal to journey order.
- One file per distinct app state; describe the state, not the action that reached it (`04_result_locked.png`, not `04_after_clicking_lock.png`).

## Shot list ordering

Order shots by user journey — what a new user sees and does first:

1. Landing view (nothing entered).
2. Main workflow end to end (fill inputs, submit, see result).
3. Secondary tabs/panels reached from the main flow.
4. Edge cases and contrasts (e.g., a failing validation next to a passing one) — number these after the happy path so they read as appendices.

Write the full shot list before running: each entry is filename + app state + interaction that reaches it. This doubles as the vignette outline.

## Embedding

- From inside `vignettes/*.Rmd`: `![](images/01_landing.png)` (relative to the vignette).
- From a root-level README: `![caption](vignettes/images/01_landing.png)`.
- Give each image a one-line caption in prose; do not restate what is visible.

## Keeping images current

- Re-run the capture script after any Shiny UI change that affects captured states.
- Do not hand-edit committed screenshots (cropping, annotation); fix the script and regenerate.
- Commit regenerated images together with the UI change so docs never drift.
