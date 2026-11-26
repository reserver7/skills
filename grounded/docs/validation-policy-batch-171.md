# Development policy validation: batch 171

This batch replayed one approved PostgreSQL migration review against three policy revisions to correct skill-selection omissions. Replays share the same fixture and are not independent scenario coverage.

| Run | Policy | Skills visibly read | Assessment |
|---|---|---|---|
| Initial | `36ca6fd752de65286c99a598b5a41bba57f544e6d5d4f56421a1f4e0b72da406` (13,423 bytes) | `requesting-code-review`, `security-and-hardening`, `database-migrations` | PostgreSQL SQL/schema review did not load `supabase-postgres-best-practices`. The cue said the specialist was used “before SQL,” which could be read as authoring-only. |
| Replay 1 | `e1e6bd13df2430ea6aff25a04f3e92e53b65e5dcdf58d140bc8691e7ce7d6a86` (13,470 bytes) | `requesting-code-review`, `supabase-postgres-best-practices`, `database-migrations` | The PostgreSQL specialist was selected, but the requested workspace-isolation review did not load `security-and-hardening`. |
| Final replay | `b0cf95bd8e22991fb8fe897ec06a8200edd9037f741bd6c739012c50380ff71c` (**13,562 bytes**) | `requesting-code-review`, `security-and-hardening`, `supabase-postgres-best-practices`, `database-migrations` | All four distinct responsibilities were covered. This was a static review with no database execution. No further routing omission was observed in this fixture. |

### Rule changes

- Clarified that the Postgres specialist applies to read-only reviews of existing SQL, schemas, and migrations, not only SQL authoring.
- Clarified that `security-and-hardening` applies when creating, migrating, or reviewing a tenant boundary or its schema, even when auth code or access policies are outside scope.
- Updated policy regression assertions. The new assertions failed before their corresponding policy clarification and passed afterward.
- No external skill body was changed.

### Final replay findings

The final agent reported three reachable OpenSpec mismatches:

1. The migration runner wraps the SQL file in a transaction, so PostgreSQL rejects its `CREATE INDEX CONCURRENTLY` statement and rolls back the migration.
2. A volatile UUID default on the new `NOT NULL` column causes a full table rewrite; the subsequent 70-million-row update is also unbounded and does not follow the approved nullable, batched-backfill plan.
3. Orphans are not preflighted or counted before the foreign key is validated. Orphan rows retain generated IDs and ordinarily cause validation to fail.

The repository fixture had no test suite or database. The review did not execute the migration. Context7 resolution was attempted on each run but quota was exhausted; the final run used the official PostgreSQL `REL_16_4` source/docs. The review also found no application code to establish compatibility of existing event inserts with the eventual `NOT NULL` column, so that point remains unverified rather than a confirmed finding. No independent reviewer was used.

### Token cost

Across the three sessions, reported usage totaled **3,506,049 input tokens** (**3,180,288 cached**), **16,682 output tokens**, and **7,756 reasoning tokens**. These are whole-session totals, including host and conversation context; they cannot be assigned to individual skills. Replaying one scenario after each rule change was expensive, so later validation should batch independent cases before changing policy when possible, then replay only cases affected by a change.

### Checks

The final setup test suite passed **49/49** on Python 3.13. The fixture `git diff --check` passed. Policy size is **13,562 bytes**, within the 14,000-byte Setup budget. Validation covers this migration-review fixture only; it does not establish globally optimal routing.
