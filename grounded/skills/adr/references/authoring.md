# ADR interview and acceptance rules

These are embedded defaults for the standalone workflow. Respect an explicit existing project ADR convention, but do not silently lower the substantive checks.

## Intent, chains and anti-monolith

- New opens an independent chain; update supersedes one specified record; deprecate-only retires a record without inventing a replacement.
- Confirm intent, scope, exact predecessor (if any), active-chain summary and anti-monolith result before interviewing.
- Count alternative entries and substantive positive/negative/adoption consequence entries for relevant active records and the draft. Do not count wrapping lines as new entries.

| Tier | Alternatives exceed | Consequences exceed | Action |
|---|---:|---:|---|
| L1 | 6 | 12 | Hint: narrow to one decision |
| L2 | 8 | 18 | Strong recommendation to split; explicit single-decision confirmation required |
| L3 | 12 | 30 | Block draft generation; split decisions or extract survey material |

Either metric triggers the highest matching tier. Below thresholds is pass. L2/L3 predecessors may supply facts, not a template that reproduces their sprawl. Existing L3 records cannot be superseded by another bundled update; choose separate new chains or deprecate-only.

## Interview branches

Ask one question at a time, recommend an evidence-backed answer, and distinguish proposal from confirmed decision. Reuse settled facts from OpenSpec and prior reviews; interview only missing or changed facts. Read code only to validate an actual claim.

### A — Context

- What happened that makes this choice necessary now? Link requirements, incidents or constraints.
- Which technical and product forces limit the options? Include team/tooling/infrastructure prerequisites.
- Can a new engineer summarize the trigger in three lines? Replace vague claims with concrete evidence.

### B — Decision

- State exactly one declarative decision, understandable out of context.
- Define the boundary: which modules, users, environments and future changes must follow it?
- Identify decider and acceptance status. “Recommended” is not “Accepted”.

### C — Consequences

- Elicit at least two distinct positive and two distinct negative consequences.
- Identify adoption/migration/operational cost, training, compatibility and rollback/escape hatch.
- Explain who bears each trade-off; do not hide product impact under a technical benefit.
- Counts are completeness prompts, not permission to invent benefits/costs. If not established, ask or fail the corresponding criterion.

### D — Alternatives considered

- At least two genuine alternatives with reasons rejected in this context.
- Include the status quo/minimum-change alternative when it was a real option.
- Explain conditions under which a rejected option would become preferable; separate evidence from assumptions.

### E — Rollout and validation

- How will the choice be adopted and validated? Link existing tasks/checks rather than copying an implementation plan.
- What can be rolled back, how, and what cannot? Include migration/compatibility constraints when relevant.
- What metric, milestone or scheduled date forces reconsideration? Name a concrete threshold/event and owner when known.

### F — References

- Link affected OpenSpec requirements/design or the existing project requirement/evidence source.
- Link related ADRs and the exact predecessor when superseding.
- Feature-local ADRs need at least one relevant requirement/design reference. Cross-cutting/global ADRs may omit a feature link only with an explicit scope statement and supporting project evidence.
- Check local references exist and are applicable/current; verify external references when their claims depend on current information. No invented pitch IDs or second source-of-truth document.

## Three adversarial personas

Each persona actively searches for gaps. Report concrete findings only. If the draft survives all checks, report that with evidence rather than fabricating the required “one gap”.

1. **New engineer (next quarter):** Can I apply this record alone? Look for vague language, implicit tooling/SDK/infra assumptions, missing rollback/escape hatch and unclear boundaries.
2. **Maintainer (two years later):** Can I tell whether it still applies? Look for absent revisit triggers, assumptions likely to expire, unsupported technical claims and missing requirement/evidence links.
3. **Product lead:** Does this preserve the product promise? Look for broken must-have requirements, hidden user/operational costs, scope creep and missing linkage to the active feature.

For each finding: persona, severity, evidence, why it matters, recommended correction. Coalesce the same finding across personas; two or more personas escalate its severity one level. Resolve critical/high gaps and recheck the affected content. Record declined recommendations with consequences; do not call unresolved blockers fixed.

## Six-criterion completeness gate

| # | Criterion | Pass condition |
|---|---|---|
| 1 | Context clear | Trigger summarized in at most three lines; no unresolved facts hidden |
| 2 | Decision singular | One declarative sentence with a clear scope |
| 3 | Consequences balanced | At least two positive and two negative consequences supported |
| 4 | Alternatives considered | At least two genuine alternatives, each with rejection reason |
| 5 | Revisit trigger | Concrete metric, milestone or scheduled review date |
| 6 | References valid | Applicable references exist and support scope; feature requirement link or explicit global scope/evidence |

Show pass/fail and evidence for every row. Preserve the threshold of five passing criteria out of six, not an invented numeric confidence score. Fewer than five or any `[TBD]` blocks writing. Critical/high unresolved findings, invalid/dangling links, missing required body sections, a bundled decision or L3 anti-monolith also block writing regardless of score. L2 additionally requires the user's explicit single-decision confirmation.

When blocked, name the failed criterion, explain exactly what answer/evidence is missing and return to that interview branch. Do not silently switch to a lighter template to bypass the gate.
