---
name: adr
description: Use when explicitly asked to author, supersede or deprecate a durable architecture decision through an interview and completeness gate.
disable-model-invocation: true
---

# ADR authoring

Preserve the interview, three-perspective adversarial review, completeness gate and append-only decision history. Use the user's language and inherited LICENSE.review-skills. OpenSpec is optional; no external pitch/config/profile system is required.

## Stage 1 — Intent and environment

Locate the project's ADR directory, naming convention, relevant active records and supersession chains. Use targeted index/title/reference searches; enumerate record metadata for the relevant scope, then read connected records. Multiple independent decisions in one domain may coexist; never treat a whole domain as a single chain.

Classify **new / update (supersede a particular record) / deprecate-only**, and feature/domain or cross-cutting scope. Confirm the intent, scope, base record/chain and anti-monolith summary with the user before proceeding. Do not infer acceptance from a recommendation. If already explicitly confirmed, reuse that confirmation.

Read [interview, persona and gate rules](references/authoring.md), including anti-monolith thresholds. Existing L2/L3 records are evidence only, not structural templates; L3 records cannot be updated as one oversized decision. Propose splitting into independent decisions or deprecating.

Deprecate-only: confirm target and reason, update only status/deprecation metadata and replacement link if applicable, then stop. Do not invent a replacement ADR.

## Stage 2 — Optional context intake

Accept relevant design notes, code, discussion, prior review and alternatives. Summarize confirmed facts, assumptions and missing decisions. Link the current OpenSpec proposal/specs/design when the decision affects an active feature; reuse established evidence instead of repeating earlier interviews. A standalone/global decision may instead reference the actual project constraints/evidence.

## Stage 3 — Interview

Follow all six branches in [the authoring procedure](references/authoring.md): context, decision, balanced consequences, alternatives, rollout/validation, references. Ask one question at a time, with a recommended answer and its evidence/assumptions. Obtain answers for consequential gaps; do not fabricate user consent, measurements or rejected options. Record [TBD] for unresolved facts and return to them before generation.

One ADR captures one declarative decision. Keep feature requirements and implementation tasks in OpenSpec or the existing plan. Do not generate another PRD/task list.

## Stage 4 — Adversarial review

Apply all three personas from the authoring procedure: new engineer, long-term maintainer, product lead. Each must actively search for at least one gap; report concrete gaps without inventing a defect in an already corrected draft. If no gap survives the checks, state the checks/evidence and that no further gap was found, rather than fabricating one.

Number findings by persona with severity/evidence. The same gap raised by two or more personas escalates one severity level, but is recorded/fixed once. Resolve critical/high findings before writing. Ask about real decision changes; incorporate supported answers and recheck affected branches.

## Stage 5 — Completeness gate

Evaluate all six criteria in the authoring procedure. Preserve the source's threshold mechanics: **5 or 6 of 6 pass**, fewer than 5 refuse; **any [TBD] refuses regardless of count**. The legacy “90%” label is a checklist name, not a mathematically exact threshold or a probability of correctness.

Apply anti-monolith checks independently: L3 blocks; L2 requires explicit confirmation that this is one decision; L1 gives a hint. Do not invent extra alternatives/consequences merely to reach counts. If evidence is insufficient, show the failing criteria and return to the relevant interview branch. Do not write the ADR on a failed gate.

## Stage 6 — Generate and hand off

Use the existing project convention, otherwise `docs/adr/YYYY-MM-DD-<slug>.md`. Avoid collisions. Use [the template](templates/adr.md); preserve context, one-sentence decision, positive/negative/adoption consequences, alternatives with rejection reasons, revisit triggers and optional exclusions.

Respect existing metadata; otherwise include date, status (Proposed unless acceptance established), scope, supersedes/deprecated state and references to actual requirements/evidence/ADRs. Validate section presence, counts, status/chain consistency and reference targets before claiming completion. Feature decisions require an applicable requirement/design reference; global decisions require an explicit scope statement and supporting evidence, not a fabricated feature link.

For supersession, write a new record and update only the predecessor's status/deprecation/replacement metadata, preserving its original rationale. Update an existing index if the project uses one; do not create a new tracking system.

Return path, gate results, accepted/unresolved consequences, supersession effect and next step. Do not implement, commit, call another review or Jev automatically. The review notes are inputs/evidence, not mandatory predecessors to standalone ADR authoring.
