---
name: plan-review
description: >
  Review and improve implementation plans before execution. Use when the user
  has an agent-generated plan for development, refactoring, analysis, migration,
  or implementation work and wants it checked for completeness, feasibility, and
  testability — even if they don't explicitly mention "plan review." Distinguish
  from code review: this skill evaluates plans, not finished code. Revise weak
  sections rather than just critiquing them.
---

# Plan Review Skill

## Purpose

Review plans created by coding agents and ensure they are complete, actionable, testable, and safe to execute. Improve the plan directly — add missing sections and rewrite weak sections rather than critiquing without action.

## Gotchas

- Do not reject plans solely for being brief. A well-scoped simple task may only need a few steps. Evaluate whether the plan's depth matches its complexity.
- When rewriting weak sections, preserve the original author's intent and structure — do not rewrite the entire plan from scratch unless it is fundamentally unsound.
- "Guidelines" references to other skills (r-code, tdd-workflow, etc.) are project-dependent. If those skills exist in the workspace, reference them; if not, note their absence as a gap rather than fabricating guidelines.
- Validation strategy must cover both automated checks (tests, linting) and manual verification steps. A plan with only one is incomplete.
- Scope exclusions are as important as inclusions. A plan that does not state what it will NOT do invites scope creep during execution.

## Required Plan Components

Calibrate depth to task complexity:

### Simple tasks (single file, obvious fix)

1. Objective — one-sentence statement of desired outcome.
2. Implementation Steps — ordered list of actions.
3. Validation Strategy — how correctness will be verified.

### Complex tasks (multi-file, refactoring, migration, new feature)

All six components required:

1. **Objective**
   - Clear statement of the desired outcome.
   - Definition of success.

2. **Scope**
   - What is included.
   - What is explicitly excluded.

3. **Guidelines**
   - Guidelines on how to produce code (refer to r-code skill).
   - Guidelines on documentation (refer to documentation and/or vignette skills).
   - Guidelines on expected tests required (tdd-workflow skill).
   - Guidelines on code formatting (linting, refer to r-code skill).
   - Guidelines on what steps may be offloaded to a sub-agent to reduce context burnout.

4. **Implementation Steps**
   - Ordered sequence of actions (i.e. To-Do list).
   - Each step should be specific and verifiable.

5. **Validation Strategy**
   - Identification of all affected code validation that tests cover every line changed.
   - Manual verification of changes.
   - Acceptance criteria of delivered code.

6. **Deliverables**
   - Files to be created or modified.
   - Expected outputs.

## Review Process

### Step 1: Read the Plan

Identify all existing sections and classify the task as simple or complex (see [references/plan-patterns.md](references/plan-patterns.md) for guidance on expected depth per plan type).

### Step 2: Check Completeness

For each required component, rank as:
- Present and sufficient
- Present but weak, or
- Missing

### Step 3: Improve the Plan

If a required component is missing:
1. Add the component using available context from the conversation and project files.
2. Populate it with concrete, specific content — not placeholders.
3. Mark any inferred details with **ASSUMPTION:** prefix.

If a component is weak:
1. Rewrite it with increased specificity (replace vague verbs like "handle" or "ensure" with concrete actions).
2. If ambiguity cannot be resolved from available context, state the assumption and proceed — do not halt for clarification.

### Step 4: Evaluate Quality

Assess whether:
- Steps are executable.
- Sequence is logical.
- Validation is adequate.
- Risks are acknowledged.
- Scope is well defined.

### Step 4b: Self-Validate

Before producing output, verify against this checklist:
- [ ] Every required component is present and populated (not left blank)
- [ ] Each step in the revised plan uses concrete, executable language
- [ ] No vague terms remain ("handle appropriately", "follow best practices")
- [ ] Scope exclusions are explicitly stated
- [ ] Validation strategy includes both automated and manual checks

If any item fails validation, revise the plan before proceeding.

## Quality Standards

Reject plans that:

- Lack testing strategy.
- Lack success criteria.
- Contain vague implementation steps.
- Ignore rollback considerations.
- Depend on unstated assumptions.

Prefer plans that:

- Are explicit.
- Are sequential.
- Are testable.
- Include risk mitigation.
- Can be executed by another agent without further clarification.

## Output Format

Produce the review using this exact structure:

### Review Summary

| Component | Status | Issue |
|-----------|--------|-------|
| Objective | Present/Weak/Missing | [brief note] |
| Scope | Present/Weak/Missing | [brief note] |
| Guidelines | Present/Weak/Missing | [brief note] |
| Implementation Steps | Present/Weak/Missing | [brief note] |
| Validation Strategy | Present/Weak/Missing | [brief note] |
| Deliverables | Present/Weak/Missing | [brief note] |

**Deficiencies:** [bullet list of issues, or "None identified"]

### Revised Plan

[Complete updated plan with all sections populated. Mark assumptions with **ASSUMPTION:** prefix.]
