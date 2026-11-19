---
name: to-tickets
description: Turn an agreed plan into independently verifiable tickets and publish approved issues to the project's tracker.
disable-model-invocation: true
---

Use the agreed plan or OpenSpec `tasks.md` as the source. Keep each ticket a thin end-to-end slice with user-visible acceptance criteria where possible. Include the source task and only the dependencies that actually block delivery.

Show the proposed titles, acceptance criteria, and blocking relationships for approval. Confirm the target tracker and project before publication. Use the project's configured tracker tooling and publish only with explicit authorization. Publish blockers first and use the resulting issue identifiers to link dependent tickets. If the tracker is unavailable, return the draft tickets.
