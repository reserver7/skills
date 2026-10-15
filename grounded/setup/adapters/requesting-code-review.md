---
name: requesting-code-review
description: Use for a requested code review or before completing a substantial or risky implementation change.
---

# Request code review

Compatibility adaptation of Superpowers 7.0.0 requesting-code-review. Setup retains the pinned upstream reviewer template beside this installed skill as `code-reviewer.md`; read it when preparing a review brief.

Use one code review for the change. Read the agreed requirements (request/chat scope or OpenSpec), actual diff including uncommitted files, connected callers/callees and relevant tests. Identify the exact base and current working state; a HEAD-only diff must not omit uncommitted work.

When authorized and available, give a fresh reviewer the requirements, changed paths, exact diff/base and focused evidence, not the whole conversation. Use the host's real reviewer/delegation facility; do not assume a Claude-specific Task tool exists. Without an authorized reviewer, perform a separate review pass and disclose the lack of independence. Do not launch agents solely because this skill is installed.

Check requirement fit, correctness, data/security risks, failure paths, meaningful test coverage and unnecessary complexity. Every finding needs a reachable failure scenario, source location and smallest fix. No style-only findings or speculative defects.

Report Critical / Important / Minor findings and a clear verdict. Fix confirmed Critical/Important issues before claiming ready; explain disagreements with evidence. Apply receiving-code-review to feedback. Re-review affected fixes rather than restarting all reviewers. Do not create a Superpowers plan, invoke Ponytail-review, or run pre-implementation plan reviews here.
