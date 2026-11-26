# Development policy validation: batch 162

This batch checks how a source-only React accessibility review routes when the environment has no React runtime, renderer, or browser test dependencies. The fixture is read-only and asks for keyboard, focus, live announcement, and accessible-name findings.

- Starting policy: `75eb9f9d9c61a2841804245fbf3268fbfc1a918923b7a02a29a78415c7465b1c` (**12,468 bytes**).
- Final policy: `60e1b0323ee508f74afa41a414f197d7b1a73733f2c41b043018c6970cc4dd35` (**12,441 bytes**, within the 12,500-byte limit).
- Runtime model: `gpt-6-luna`, medium reasoning, fresh disposable read-only runs. The host had no `react`, `react-dom`, `react-test-renderer`, or Testing Library packages; no packages were installed.

| Replay | Observed route and result | Finding |
|---|---|---|
| Initial source-only review (`75eb9f9d…`) | Read the component and project guidance, but selected no skill because no running page or accessibility tree was available. It still identified the non-semantic clickable `div`, missing live announcement, focus loss risk, and label issues, and separated runtime-only claims. No files changed. | A browser is unnecessary for source-supported UI/accessibility findings. The general UI review trigger was too easy to skip when the source was present without a rendered page. |
| Same review on the clarified rule (`60e1b032…`) | Selected `web-design-guidelines` only, read its fixture copy, and reported supported findings for keyboard semantics, focus, count announcements, and labels. It marked keyboard traversal, actual focus landing, and screen-reader announcements as requiring browser/runtime evidence. No code or docs inside the fixture changed; diff check passed. | Source-only UI audits now trigger the specialist, while runtime claims remain bounded by available evidence. |

### Policy change carried forward

The UI/accessibility trigger now explicitly includes source-only component audits: use `web-design-guidelines` even when no page is running; use the source for code-supported findings and reserve behavior claims for runtime/browser evidence. React framework implementation remains separately routed to `vercel-react-best-practices` when framework semantics matter.

Two runtime sessions reported **257,205 input tokens** (211,200 cached), **1,724 output tokens**, and **245 reasoning tokens**. These are whole-session figures with host and conversation context, not skill-specific costs.

The source audit does not establish actual keyboard behavior, rendered focus movement, screen-reader announcements, or React component lifecycle. Those remain unverified because this fixture environment lacks the runtime dependencies and browser harness. No application files, packages, production systems, or upstream skill bodies were changed.

### Final checks

The final development policy is still **12,441 bytes** with SHA-256 `60e1b0323ee508f74afa41a414f197d7b1a73733f2c41b043018c6970cc4dd35`. Repository checks passed: Grounded setup suite **41/41**, `manage.py check`, local validator compilation and `--help`, `git diff --check`, and **147** local Markdown links across the validation index and recent archives (no broken links). These checks confirm repository/setup integrity; they do not replace the unavailable React/browser runtime check.
