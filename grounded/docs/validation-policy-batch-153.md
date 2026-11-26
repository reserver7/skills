# Development policy validation: batch 153

This is a new validation series after batch 152. It evaluates adaptive skill routing across integrated engineering work; scenarios are probes, not a fixed routing table.

## Policy and method

- Starting policy: `3cfb6497b717386e512945b3c14afc949a060f0848cf205a3a73f27733baa6f6` (batch 152).
- Final policy: `3c9daa2c37e26c5af15caf67d7d18790e222835ce5c72f7a579a76d24ab5def5`, **10,857 bytes**. Setup accepts up to 12,000 bytes.
- Runtime model: `gpt-6-luna`, medium reasoning, fresh ephemeral runs and disposable Git fixtures. The final five-case cohort used the same final policy hash. External skill bodies were copied into each fixture; the last run's selected skill files matched their prepared hashes.
- Network was available, but the harness used `--ignore-user-config`, so host MCP servers (including Context7) were not exposed inside those runs. Exact official documentation fallback remained available in principle.
- JEV assessment was attempted three times; the tool returned HTTP 422, 400, and 422 without an assessment. The observations below are direct runtime evidence, not a JEV result.

## Initial cross-domain cohort

The first nine probes ran on the starting policy and motivated the replays below. Their combined session usage was **4,577,939 input tokens** (cached input included) and **34,353 output tokens**. These totals include the host and conversation context and cannot be assigned to skill selection or individual skills.

| Work type | Observed route and result | Signal |
|---|---|---|
| Read-only UI/accessibility audit | `web-design-guidelines` only; source findings were separated from browser/runtime checks. No edits or tests. | Good narrow selection. |
| React + Supabase realtime integration | Initially missed the React specialist; Context7 was unavailable. Later replays exposed repeated `ctx_resume` calls and incomplete lifecycle evidence. | Specialist omission and context/tool overhead. |
| Next.js tenant-auth defect | Debugging, security, TDD, and review guidance were used; four focused tests passed. Completion verification overlapped the review procedure. | Good defect/security coverage; workflow duplication. |
| New API plus documentation | API design, security, TDD, and doc-updater were used; debugging was initially added to a new feature. A replay omitted debugging and passed six focused tests. | Keep debugging tied to an existing defect; documentation skill can be selective. |
| CI plus progressive production rollout | CI/CD and deployment specialists covered distinct work; TDD and completion verification were also selected. Official docs were used after Context7 failed; no live deployment occurred. | The CI/rollout combination was justified; completion verification was redundant. |
| Privacy-sensitive telemetry | Observability, security, and TDD; five focused tests passed. | Distinct telemetry and privacy roles. |
| MySQL migration | ECC migration and MySQL specialists plus review guidance. Exact 8.4.3 runtime evidence was absent and the Docker daemon was unavailable. | Correct domain split; database/runtime claim kept limited. |
| PM ticket decomposition | `to-tickets` only; local draft, no remote publication. | Good no-code route. |
| Read-only API QA audit | Early replay inferred Supabase/debugging from alert terminology without matching artifact evidence. Later replay corrected to the contract/security review path. | Select from inspected behavior and data path, not feature labels. |

## Policy changes informed by the cohort

The rules were tightened without adding a scenario-to-skill matrix or changing any upstream skill body:

1. Before choosing skills, inspect only the relevant spec/decision and target code/configuration evidence. Reconcile the selected roles against only matching domain-owner and material-risk cues in the actual behavior path. Include matching roles even when their enforcement layer is not edited; do not scan unrelated skills.
2. Ground framework/service/database choices in files and dependency evidence, not names such as “alerts” or “events.” React and Supabase ownership cues are explicit for behavior that actually uses their APIs.
3. Apply Grounded's task triggers when deciding whether to load a workflow skill. A broad description or generic “always” wording does not expand the trigger; once loaded, follow the original skill instructions unchanged.
4. Keep fresh-task context separate from interrupted-task recovery. The harness states that each run is fresh; `ctx_resume` is only for an identified interrupted task with a recoverable record.
5. A helper test proves only the helper boundary. A hook, route, or integration lifecycle remains unverified unless a check exercises that boundary.
6. Versioned APIs require Context7 before dependent work, then an exact official tag/release/package fallback if Context7 is unavailable. A spec or current unversioned documentation is not proof of pinned-version support.

## Final-policy replays

Five isolated cases were run on final fingerprint `3c9daa2c…`. Their combined usage was **2,554,826 input tokens** (2,281,984 cached) and **22,517 output tokens**. These are whole-session figures, not per-skill costs.

| Case | Selected skills evidenced in the fixture | Result and limits |
|---|---|---|
| Approved React/Supabase workspace-event implementation | `api-and-interface-design`, `security-and-hardening`, `supabase`, `vercel-react-best-practices`, `test-driven-development`, `requesting-code-review` | Focused tests **2/2**, diff check clean. No `ctx_resume`; no debugging, Ponytail, or completion-verification call. Filter and cleanup API behavior were checked against official current Supabase/React docs, but the exact `@supabase/supabase-js@2.52.0` artifact could not be fetched. Hook lifecycle and live RLS were not tested. A separate requirements/diff pass occurred; it was not independent. The implementation proceeded despite the unavailable exact package evidence, contrary to the policy's pause gate; record this as an execution failure, not as a need to repeat the rule. |
| Read-only Orders UI accessibility audit | `web-design-guidelines` only | Actionable source findings cited; browser-only checks separated. No edits or tests. No implementation/design skill was added. |
| Approved alert-spec ticket draft | `to-tickets` only | Testable tickets and dependencies drafted from the approved contract. No file edits or remote publishing. |
| Read-only `/v2/alerts` contract QA | `api-and-interface-design`, `security-and-hardening`, `requesting-code-review`, `verification-before-completion` | Correctly identified the absent endpoint and docs. Existing test command exited 0 but discovered **0 tests**; this was reported as no behavioral coverage. No debugging or Supabase inference. No `ctx_resume`. |
| Approved progressive production rollout | `ci-cd-and-automation`, `deployment-patterns`, `test-driven-development`, `requesting-code-review` | Focused tests **6/6**, diff check clean. No completion-verification or debugging call; no live deployment. Exact Node and action-major documentation was checked via official sources because Context7 was unavailable. Review pass was separate but not independent. No `ctx_resume`. |

All five used the final policy fingerprint, had zero tool-argument errors, and left the source repository untouched; implementation edits were confined to disposable fixtures. The QA result correctly distinguishes an empty test suite from a passing behavior check.

## Remaining evidence limits

- Context7's monthly quota was exhausted when checked from the main environment. In addition, the isolated harness disables host MCP configuration. The final React/Supabase run therefore used current official web documentation, and its exact pinned package artifact was unreachable. Because the policy already says to stop dependent work when exact evidence is unavailable, no further policy wording was added for this noncompliance. Re-run this dependency-specific route only in an environment where the exact official artifact can be reached.
- The final five are a targeted cross-domain replay, not a statistical benchmark or proof that every skill and host combination is perfect. The earlier nine are retained as historical evidence from the starting fingerprint.
- Session token totals are large and include host/conversation context. They are useful as a cost warning but do not establish how many tokens were caused by Grounded or a particular skill.
- No JEV result is available for this batch.

## Repository checks

- `rtk python3.13 -m unittest test_manage`: **27/27 passed** after the policy and setup-limit changes.
- `rtk git diff --check`: passed.
- Current policy size: **10,857 bytes**; configured setup maximum: **12,000 bytes**.
- No release, commit, push, live deployment, or upstream skill modification was performed.
