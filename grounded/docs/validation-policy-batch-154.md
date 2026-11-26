# Development policy validation: batch 154

This policy delta follows the five-path runtime cohort in [batch 153](validation-policy-batch-153.md). It makes the optimization objective explicit: maximize task quality while minimizing duplicate skill, context, and check work, without dropping anything required for correctness, risk, or user-requested coverage.

- Previous runtime fingerprint: `3c9daa2c37e26c5af15caf67d7d18790e222835ce5c72f7a579a76d24ab5def5`.
- Current policy fingerprint: `0214d804ce0f49b72d0f399c65180e615ae7e64ad87c64c8089812449d553cd0`, **11,304 bytes**; setup maximum is **12,000 bytes**.
- Added rule: use the smallest sufficient distinct skill/check set, carry valid evidence forward, rerun only for changed behavior, prior misses, uncovered risk, or broader coverage the user explicitly requests. Token savings never justify omitting needed expertise or verification.
- Static verification: `rtk python3.13 -m unittest test_manage` passed **28/28**; `rtk git diff --check` passed.
- No new Luna scenario was run. The wording does not change skill triggers, and batch 153 already exercised the relevant routes. Replaying those same cases would add substantial whole-session token use without testing a changed route. Thus this delta has static policy-test evidence, not fresh runtime evidence.
- No external skill body was modified. No commit, release, or push was made.
