# Validation record

**English** | [한국어 요약](validation.ko.md)

This page is the concise index. Detailed scenario evidence is split into date-based archives below. These are historical observations from the listed policy, host, model, and fixture states; they are not current routing instructions. Follow [the active development policy](../rules/development.md) for current behavior.

No full agent-quality benchmark or fresh physical-machine integration run has been performed. Batch 163 verified installation into a clean temporary Codex home. The recorded runtime samples and static checks do not establish overall quality parity or token savings. Session token totals include host and conversation context and cannot be attributed to Grounded or to individual skills.

## Detailed records

| Date | Coverage | Archive |
|---|---|---|
| October 19–20, 2026 | Initial runtime scenarios, cross-domain work, procedure restoration, replay/idempotency, and policy/release checks | [October archive](validation-2026-10.md) |
| November 20, 2026 | React/UI smoke, repository-wide routing, cross-domain and tool-boundary scenarios | [November 20 archive](validation-2026-11-20.md) |
| November 21, 2026 | Setup lifecycle, concurrency/recovery, and natural skill-routing batches | [November 21 archive](validation-2026-11-21.md) |
| November 22–23, 2026 | Cross-domain skill-routing batches 4–37 | [November 22–23 archive](validation-2026-11-22-23.md) |
| November 24, 2026 | Historical batches 38–70 | [November 24 archive](validation-2026-11-24.md) |
| November 24, 2026 | Previous policy, batches 71–123 | [Previous-policy archive](validation-current-policy-2026-11-24.md) |
| November 25, 2026 | Previous policy, batch 124 | [Batch 124 archive](validation-policy-batch-124.md) |
| November 25, 2026 | Previous policy, batches 125–133 | [Batches 125–133](validation-policy-batch-125.md) |
| November 25, 2026 | Previous policy, batches 134–143 | [Batches 134–143](validation-policy-batch-134.md) |
| November 25, 2026 | Previous policy, batches 144–149 | [Batches 144–149](validation-policy-batch-144.md) |
| November 25, 2026 | Initial closure comparison, batch 150 | [Batch 150](validation-policy-batch-150.md) |
| November 25, 2026 | Focused interaction, decision, and review replays, batch 151 | [Batch 151](validation-policy-batch-151.md) |
| November 25, 2026 | Final blocked-decision replay, setup gate, and closure, batch 152 | [Batch 152](validation-policy-batch-152.md) |
| November 25, 2026 | Integrated engineering routing across frontend, API/security QA, PM, Supabase, and CI/rollout, batch 153 | [Batch 153](validation-policy-batch-153.md) |
| November 25, 2026 | Quality-per-token policy delta; static policy checks, batch 154 | [Batch 154](validation-policy-batch-154.md) |
| November 25, 2026 | Code-heavy integrated engineering cohort on policy `0214d80…`, batch 155 | [Batch 155](validation-policy-batch-155.md) |
| November 25, 2026 | Targeted React/Supabase, authorization, and rollout replays on policy `5c850db…`, batch 156 | [Batch 156](validation-policy-batch-156.md) |
| November 25, 2026 | Risk-based test-first rule and focused replays on policy `dcc83cb…`, batch 157 | [Batch 157](validation-policy-batch-157.md) |
| November 25, 2026 | Blocker-scoped progress and injected Supabase owner replay on policy `8415686…`, batch 158 | [Batch 158](validation-policy-batch-158.md) |
| November 26, 2026 | Requested-target ownership, auth review, ignored OpenSpec discovery, skill-catalog restraint, and narrow code-fix replays on policy `7dadf29…`, batch 159 | [Batch 159](validation-policy-batch-159.md) |
| November 26, 2026 | Skill-free preflight, public API TDD, coordinated documentation, and duplicate-test restraint on policy `e2dec63…`, batch 160 | [Batch 160](validation-policy-batch-160.md) |
| November 26, 2026 | Blocked-slice skill restraint, direct approval handoff, and proportional TDD on policy `75eb9f9…`, batch 161 | [Batch 161](validation-policy-batch-161.md) |
| November 26, 2026 | Source-only React accessibility review routing and evidence boundaries on policy `60e1b032…`, batch 162 | [Batch 162](validation-policy-batch-162.md) |
| November 26, 2026 | React browser interaction replay, clean Codex installation, and setup budget boundary, batch 163 | [Batch 163](validation-policy-batch-163.md) |
| November 26, 2026 | Narrowed completion-verification trigger and focused-test routing replay, batch 164 | [Batch 164](validation-policy-batch-164.md) |
| November 26, 2026 | Ponytail, OpenSpec, and Superpowers verification-route cohort, batch 165 | [Batch 165](validation-policy-batch-165.md) |
| November 26, 2026 | OpenSpec/Superpowers/domain-specialist combinations and review-route correction, batch 166 | [Batch 166](validation-policy-batch-166.md) |
| November 26, 2026 | Public API + OpenSpec/Superpowers routing and structured-input verification correction, batch 167 | [Batch 167](validation-policy-batch-167.md) |
| November 26, 2026 | React/Superpowers review, CI rollout/security routing, and skill-reporting correction, batch 168 | [Batch 168](validation-policy-batch-168.md) |
| November 26, 2026 | Blocked OpenSpec/Superpowers routing, sequential decisions, and exact-source fallback, batch 169 | [Batch 169](validation-policy-batch-169.md) |
| November 26, 2026 | Cross-tenant cache bug-fix skill combination, batch 170 | [Batch 170](validation-policy-batch-170.md) |
| November 26, 2026 | PostgreSQL migration-review specialist routing and tenant-boundary security replay, batch 171 | [Batch 171](validation-policy-batch-171.md) |
| November 26, 2026 | Approved API bug fix with explicit OpenSpec and Superpowers, batch 172 | [Batch 172](validation-policy-batch-172.md) |
| November 26, 2026 | Superpowers-only routing, TDD red evidence, completion-check overuse, and artifact cleanup, batch 173 | [Batch 173](validation-policy-batch-173.md) |
| November 26, 2026 | Approved API bug fix with explicit OpenSpec and Superpowers, batch 172 | [Batch 172](validation-policy-batch-172.md) |

## Reading the evidence

Each archive records the observed route, outcome, checks, limits, and session costs when available. Policy-specific archives are fingerprinted: compare each batch only with its development-rule revision and stated environment, and start a new series when the fingerprint changes. A pass applies only to the stated fixture and environment. Partial or blocked outcomes remain visible; reruns are not independent evidence unless the record says so. The Korean page is a concise summary, while these archives preserve the detailed English session records.
