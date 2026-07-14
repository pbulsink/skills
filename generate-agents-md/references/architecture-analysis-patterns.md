# Architecture Analysis Patterns for R Packages

Detailed guidance for analyzing `R/*.R` files to extract architecture information
for AGENTS.md generation. Use these patterns in Step 3 of the skill process.

---

## File Role Heuristics

Determine each file's conceptual role using a combination of filename convention,
roxygen structure, and function signatures:

### Naming Convention Patterns

| Filename Pattern | Typical Role | Notes |
|-----------------|--------------|-------|
| `zzz.R` | Package lifecycle hooks | `.onAttach`, `.onLoad`, `.onUnload` — startup/shutdown code |
| `aaa-*.R` or `zzz-*.R` | Sort-priority helpers | Load early/late; often shared constants, options, or base validators |
| `*-package.R` | Package-level documentation | Namespace imports (`@importFrom`), internal keywords, usually just `NULL` |
| `data.R` | Dataset definitions | `@examples` data loading, `@format` dataset descriptions, `@exportData` |
| `utils*.R` or `util*.R` | Internal helper functions | Validators, formatters, shared logic not user-facing |
| `{verb}*.R` (e.g., `io.R`, `plot.R`) | Feature module | Exported API surface; each file is a capability area |

### Content-Based Role Detection

When filename alone is ambiguous, inspect the roxygen documentation:

1. **Count `@export` tags** per file — files with 3+ exports are likely feature modules
2. **Read first roxygen block** of the file — the `@description` often states the module's purpose
3. **Check for internal-only functions** — if all functions use `@keywords internal`, the file is infrastructure

### File Role Classification

Classify each file into one category:

- **Core API**: Contains exported functions that form the primary user interface
- **Data I/O**: Reads external formats, writes output files, handles serialization
- **Transformation**: Modifies data (maths, normalization, conversion between representations)
- **Visualization**: Generates plots or visual output
- **Analysis**: Statistical methods, peak detection, fitting algorithms
- **Infrastructure**: Validators, helpers, startup hooks, shared constants

---

## Function Analysis Patterns

### Extracting Exported Functions

For each roxygen block followed by a function definition:

```r
#' @description One-sentence summary of what this does.
#'   Bilingual translation if present (skip for the AGENTS.md table).
#' @param x Description of parameter x.
#' @return What this returns.
#' @export
my_function <- function(x, y = NULL) { ... }
```

Extract:
- **Name**: `my_function`
- **Parameters**: `x`, `y` (note defaults and types from roxygen `@param`)
- **Purpose**: First sentence of `@description`
- **Returns**: Content of `@return` block

### Identifying Internal Helpers

Internal functions follow these patterns:

1. Named with dot prefix: `.internal_helper()` — convention for private helpers
2. No `@export` tag in roxygen block AND not referenced by any exported function's `@seealso` or examples
3. Defined in the same file as an exported function that calls it (co-located helper)

Only include internal functions in the AGENTS.md output if they:
- Are called from multiple exported functions (shared utility)
- Implement non-obvious logic worth documenting for agents
- Have a role that affects how the public API works (e.g., a validator that defines data format requirements)

### Function Signature Conventions

Common R package function signature patterns to recognize:

```r
# Standard — data first, options last
process_data <- function(data, method = "default", ...) { ... }

# ggplot2-style — plot object + layer additions
annotate_plot <- function(plot, xintercept, linetype = "solid") { ... }

# Builder pattern — returns modified object
add_marker <- function(plot, wavenumber, text = NULL) { ... }  # returns modified ggplot

# Pipe-friendly — first arg is data, piped in via {.} or explicit
transform_spectra <- function(spectra, operation, params = list()) { ... }

# S3 generics with methods
print.MyClass <- function(x, ...) { ... }
```

---

## Dependency Analysis

### Tracking Package Dependencies

From `R/*.R` files, collect all package references:

1. **Direct namespace calls**: `pkg::function()` — always count as a dependency
2. **requireNamespace() guards**: `if (!requireNamespace("pkg", quietly = TRUE))` — soft dependency, only loaded when needed
3. **@importFrom in roxygen**: `#' @importFrom pkg func` — hard import declared at package level

Classify each dependency:

| Type | Indicator | Impact |
|------|-----------|--------|
| Hard import | In DESCRIPTION `Imports:` or `@importFrom` | Always available, part of core API surface |
| Soft dependency | `requireNamespace()` guard in code | Optional feature; function errors if missing |
| Suggested only | In DESCRIPTION `Suggests:`, no `::` calls in code | Available for development/tests but not runtime |

### Data Object Tracking

From `data/` directory and roxygen docs:

1. List `.rda` / `.RData` files in `data/`
2. Check if a corresponding `@format` or `@docType "data"` block exists in `R/data.R`
3. Infer purpose from the dataset name (e.g., `biodiesel.rda` → biodiesel fuel spectra data)
4. Cross-reference with vignette usage to confirm actual use cases

---

## Architecture Summary Table Guidelines

### Filling the Role Column

Be specific but brief. One sentence, no articles if possible:

```
✓ Core plot generation with overlaid and stacked layouts
✗ This file contains the main plotting functions for FTIR spectra
```

### Filling the Key Functions Column

- List only **exported** functions that form the public API surface of that module
- Use backtick-wrapped function names: `fn_name()`
- Omit internal helpers, S3 methods (unless they are the primary interface), and functions with `@keywords internal`
- Limit to 3–5 key functions per row; if there are more, list the most user-facing ones

### Table Ordering

Sort rows alphabetically by filename. Group files that are conceptually related on adjacent lines when alphabetical order would separate them (e.g., `aaa-shared_params.R` stays at top due to naming convention).

---

## Gotchas for R Package Analysis

- **Roxygen blocks may span multiple lines** with both English and French — extract only the first sentence of `@description` for brevity. Skip translations unless they contain materially different information.
- **S3 generics** have their generic in one file (`R/plot.R` defines `plot_ftir()`) and methods in another (`R/plot-classes.R` defines `print.PlotFTIR_plot`). Attribute the method to the module where its generic is defined for the architecture table.
- **Namespace imports via `@importFrom`** may appear in `-package.R` files rather than individual function files. Check those when compiling dependencies.
- **`.Rd` files in `man/` are generated**, not source — do not analyze them. They reflect roxygen comments already present in `R/*.R`.
- **`NAMESPACE` file is auto-generated** by roxygen2 — its contents mirror the `@export` tags and `@importFrom` directives in R source files, but it should not be used as a primary analysis source since it may lag behind development.
