---
name: grill-me
trigger: stress-test plans, decisions, or ideas; challenge thinking
description: >-
  This skill should be used when the user wants to stress-test their thinking
  before committing resources. Triggers on phrases like "grill me," "challenge my
  plan," "stress-test this idea," "help me think through a decision," "poke holes
  in my approach," or any request to rigorously evaluate plans, decisions, designs,
  or ideas — even if the user does not explicitly mention those terms.
metadata:
  category: productivity
  source:
    repository: 'https://github.com/mattpocock/skills'
    path: skills/productivity/grilling/SKILL.md
    license: MIT
---

# Grill Me

Conduct a rigorous stress-test interview on the user's plan, decision, or idea. Walk down every branch of the decision tree, resolving dependencies one at a time. For each question, provide a recommended answer.

## Workflow Progress

- [ ] Identify all decisions and assumptions in the plan
- [ ] Start with the highest-level decision; drill into sub-decisions recursively
- [ ] Ask questions one at a time — never ask multiple questions in a single message
- [ ] For each question, provide your recommended answer before asking
- [ ] Resolve dependencies between decisions sequentially (do not skip unresolved branches)
- [ ] Look up facts from the environment (filesystem, tools) instead of asking
- [ ] Present *decisions* to the user and wait for their response — do not assume
- [ ] Continue until a shared understanding is reached

## Procedure

1. Identify all key decisions, assumptions, and dependencies in the plan or idea presented.
2. Start with the highest-level decision. Ask one question about it, provide your recommended answer, then wait for the user's response.
3. After resolving each decision, identify sub-decisions or dependencies it introduces. Drill into those next before moving to other branches.
4. Repeat until all branches of the decision tree are resolved and a shared understanding exists.

### Fact-finding vs Decision-making

- If information can be obtained by exploring the environment (filesystem, tools, existing code), look it up directly rather than asking the user.
- For decisions that require judgment or preference — present each one individually with your recommended answer and wait for confirmation.

## Gotchas

- **Never ask multiple questions at once.** This overwhelms the user. Ask one question, provide a recommendation, then pause.
- **Do not skip unresolved dependencies.** If decision A depends on decision B, resolve B first before proceeding down A's branch.
- **Distinguish facts from decisions.** Facts are discovered; decisions are made by the user. Do not confuse the two or make assumptions about user preferences.
- **Provide a recommended answer with every question.** The interview is collaborative — silence without guidance reduces its value.
- **Do not act on the plan until shared understanding is confirmed.** The goal is thinking, not execution.
