---
name: craft-anything
description: Use only when the user explicitly asks to use Craft Anything to study or rebuild a reference website, app, or game for an authorized personal portfolio project.
disable-model-invocation: true
---

# Craft Anything

Use Craft Anything only for an explicitly requested reference-study or recreation workflow. It is an early-alpha tool. It is not the default workflow for ordinary product development; use the project's requirements and implementation workflow for that.

## Before starting

- The Grounded-managed command is available at the path supplied in the Grounded setup section below. Run `doctor` first and read its result. If the installed coding-agent adapter is unsupported or fails, use Craft Anything only to collect study evidence and continue implementation with the active coding agent.
- Work only on software the user owns or is authorized to examine. Keep the project in the user-designated directory and inspect existing files before writing. Do not overwrite an existing project without the user's explicit request.
- For third-party references, keep the workflow in clean-room mode. Do not inspect or copy source code, private files, credentials, or protected content. Recreate general layout and interaction ideas; do not reuse logos, photos, text, or other assets without permission.
- Treat generated output as a draft. Inspect the result and summarize what was studied, generated, and left for follow-up.

## Workflow

1. Confirm the reference and the destination project from the user's request. Ask only if either is ambiguous in a way that affects access or overwriting.
2. Run `doctor` and use the installed CLI's help to confirm the current command syntax.
3. Use the Study → Build → Check → Ready workflow for the requested website, app, or game. Keep evidence and generated files within the requested project.
4. Review the output with the project's existing checks. Do not claim that Craft Anything's checks replace the project's tests or browser QA.

## Grounded setup

Grounded installs and verifies the official CLI and appends its managed executable path here. Run Craft Anything only through that executable.
