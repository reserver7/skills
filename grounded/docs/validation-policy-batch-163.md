# Development policy validation: batch 163

This batch closes two evidence gaps identified after batch 162: actual browser interaction for the React accessibility fixture, and installation into a clean Codex home. It also adds space to the setup policy-size ceiling without changing the policy text.

- Development-policy SHA-256: `60e1b0323ee508f74afa41a414f197d7b1a73733f2c41b043018c6970cc4dd35` (**12,441 bytes**, unchanged).
- Setup policy ceiling: raised from **12,500** to **14,000 bytes**. This does not add prompt text; the current policy retains **1,559 bytes** of headroom.
- Runtime fixture: disposable local React `19.3.1` and `react-dom` `19.3.1`, bundled by esbuild `0.28.1`; browser operated with the installed Playwright CLI `0.1.25`. No project dependencies or source files were changed.

| Check | Result | What it establishes |
|---|---|---|
| Browser review of the batch 162 `NotificationMenu` fixture | `web-design-guidelines` remained the sole review skill. Playwright rendered the React component, opened the menu, tabbed through the page, activated the action by mouse, and inspected the DOM focus and announcement regions. | Tab skipped the generic “Mark all read” item and landed on the following link. Clicking the item updated the count to zero and closed the menu, but focus fell to `body`. No `aria-live`, `role=status`, or `role=alert` region existed. These are reproduced interaction findings; no claim about assistive-technology speech was made. |
| Fresh isolated Codex installation | `manage.py setup --host codex --home <temporary-home>` exited 0 and installed Grounded **0.6.1**, managed skills, dependencies, and Chromium in the temporary home. `manage.py version` reported package and applied policy `0.6.1`; `manage.py doctor` reported repository structure, managed skills, policy, dependency receipt, and overlap checks passed. | Clean-home integration passed for this macOS Codex environment. The user's global home and project dependencies were untouched. This is not a fresh-device or Claude-host test. |
| Policy ceiling boundary | Added tests failed before implementation because `validate_policy_budget` did not exist; after adding the helper, **14,000 bytes passed** and **14,001 bytes failed** as expected. | The configured ceiling has a tested inclusive boundary. |

The browser check confirms the source-only findings from batch 162 and bounds them with runtime evidence. The setup check resolves the clean-home install gap for one host. No new skill-routing failure appeared, so the development policy itself was not changed. External skill bodies were installed from their resolved sources and were not edited.

### Final checks

Grounded setup tests passed **43/43**, including the two new policy-budget boundary tests. `manage.py check`, temporary-home `doctor`, validator compilation and `--help`, **150** local Markdown links (no broken links), and `git diff --check` passed. The development policy remains 12,441 bytes at the recorded SHA.

### Limits

This batch does not establish accessibility behavior across other browsers or screen readers, every Grounded skill route, a fresh physical machine, or Claude-host installation. Those are broader coverage goals, not failures found in this batch. The UI was a synthetic fixture, not an application owned by the user.
