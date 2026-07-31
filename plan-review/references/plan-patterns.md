# Plan Patterns Reference

Reference material for calibrating expected depth and completeness of plans by task type. Load when evaluating whether a plan's scope matches its complexity.

## Simple Bugfix

**Scope:** Single file, one or two functions, obvious root cause.

**Expected components:** Objective (1 sentence), Steps (3-5 actions), Validation (test + manual check).

**Typical depth:** 200-400 words total. No Guidelines section needed unless project conventions are non-standard.

**Example triggers:** "Fix the null pointer in parseDate", "Update the error message on line 42".

## Feature Implementation

**Scope:** New functionality spanning multiple files or modules. Requires design decisions and integration points.

**Expected components:** All six (Objective, Scope with exclusions, Guidelines, Steps, Validation, Deliverables).

**Typical depth:** 500-1500 words. Should include API surface discussion, data flow diagrams if applicable, and migration considerations for persistent changes.

**Example triggers:** "Add user export to CSV", "Implement webhook handler for payment events".

## Refactoring

**Scope:** Restructuring existing code without changing external behavior. High risk of introducing regressions.

**Expected components:** All six required. Scope exclusions are critical — must explicitly state what behavior must NOT change. Validation strategy should emphasize regression tests and property-based checks.

**Typical depth:** 400-1200 words. Should include before/after structure comparison, risk assessment for each refactoring unit, and rollback plan if tests fail after a step.

**Example triggers:** "Extract the database layer into a separate module", "Replace nested conditionals with strategy pattern".

## Migration

**Scope:** Transitioning between versions, formats, dependencies, or platforms. Highest risk category — requires explicit rollback procedures.

**Expected components:** All six required plus explicit rollback plan. Guidelines section must cover backward compatibility and data integrity.

**Typical depth:** 800-2500 words. Should include version matrix, compatibility notes, data migration scripts, testing strategy for both old and new states, and a phased rollout plan if applicable.

**Example triggers:** "Migrate from R 4.3 to R 4.5", "Switch from devtools to pak for package management".

## Analysis / Research

**Scope:** Investigating a problem space, comparing options, or gathering information to inform future decisions. Output is informational rather than code.

**Expected components:** Objective (with decision criteria), Scope, Steps (research methodology), Validation (how conclusions will be verified). Guidelines and Deliverables may be adapted for non-code output.

**Typical depth:** 300-800 words. Should specify data sources, evaluation criteria for comparisons, and how findings will be communicated.

**Example triggers:** "Research best practices for R package testing", "Compare serialization formats for our use case".

## Common Deficiencies by Plan Type

| Plan Type | Most Common Omission |
|-----------|---------------------|
| Bugfix | No regression test added |
| Feature | Scope exclusions not stated (leads to scope creep) |
| Refactoring | Rollback plan absent; behavior change boundaries unclear |
| Migration | Backward compatibility testing missing |
| Analysis | Decision criteria not defined (findings lack actionable output) |
