---
name: evaluating-r-test-coverage
description: Measures R package test coverage using covr, exports standard Cobertura XML format, and identifies untested lines or low-coverage functions.
tools:
  - execute_bash
  - read_file
---

## Overview

Use this skill to evaluate code coverage for R packages. It executes `covr::package_coverage()` in a subprocess, converts the output to Cobertura XML using `covr::to_cobertura()`, and parses the results to evaluate package quality against target coverage thresholds.

---

## Workflow

### 1. Execute Coverage Analysis

Run the following R command from the package root directory using an isolated R process:

```bash
Rscript -e '
  suppressPackageStartupMessages(library(covr));
  cov <- package_coverage();
  to_cobertura(cov, filename = "coverage.xml");
  cat(sprintf("Overall Coverage: %.2f%%\n", percent_coverage(cov)))
'
```

> **Note:** For large packages or slow test suites, run `covr::file_coverage()` on modified source files rather than full package coverage during quick iterative loops.

---

### 2. Parse Cobertura Output

Read `coverage.xml` to inspect class-level and line-level coverage.

* **Overall Line Rate:** Look for `line-rate="..."` in the root `<coverage>` tag (e.g., `line-rate="0.852"` = 85.2% coverage).
* **Uncovered Lines:** Look for `<line number="X" hits="0"/>` under specific `<class filename="...">` blocks.

---

### 3. Coverage Analysis Rules

When summarizing results for the user or workflow:

1. **Threshold Checks:**
   * **Target Met (≥ 80% default):** Mark coverage check as passing. Highlight any critical business logic lines missing coverage.
   * **Target Failed (< 80%):** List specific functions or files driving down the percentage.

2. **Exclusions & Edge Cases:**
   * Do not penalize low coverage on auto-generated code (`R/cpp11.R`, `R/RcppExports.R`) or legacy C/C++ code unless explicitly requested.
   * Check if inline exclusions (e.g., `# nocov start` ... `# nocov end`) are used appropriately.

3. **TDD Feedback Loop:**
   * Identify lines with `hits="0"` added or modified in the current branch.
   * Output targeted recommendations for missing unit tests in `tests/testthat/`.

---

## Common Commands & Snippets

### Quick Single-File Coverage
```r
covr::file_coverage(
  source_files = "R/my_function.R",
  test_files = "tests/testthat/test-my_function.R"
)
```

### Excluding Files Programmatically
If the package requires excluding specific directories (e.g., legacy scripts):
```r
cov <- covr::package_coverage(line_exclusions = list("R/deprecated.R"))
covr::to_cobertura(cov, filename = "coverage.xml")
```

---

## Output Format

Report coverage back to the user or system with the following summary structure:

* **Overall Package Coverage:** `XX.X%`
* **Coverage Status:** `PASS` / `WARN` / `FAIL`
* **Top Uncovered Areas:**
  * `R/filename.R`: Lines 42-50 (`function_name()`)
  * `R/utils.R`: Lines 12, 18 (`helper_fn()`)
* **Recommended Actions:** Concrete suggestions for `testthat` blocks to add.
