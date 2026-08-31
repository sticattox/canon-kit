# canon-kit specification

A knowledge system is a set of typed tables plus a router. Models generate and edit rows. Scripts verify writes. Humans correct. Corrections outrank old rows.

## Authority order

1. The operator's current instruction or correction
2. The current canonical artifact for that fact
3. The active procedure
4. Verified system state
5. Stored interpretation
6. Handoff or summary
7. Memory or assumption

Preference is not belief. Hypothesis is not fact. Correction is not overwrite. Example is not rule.

## Hard rules

### R1. One fact, one canonical home

Every durable fact lives in exactly one editable table or document. Other files may link to it. They may not independently edit a copy.

Frozen snapshots may duplicate rows for history. Mark them `FROZEN` and read-only.

### R2. Provenance is not optional

Keep these classes distinguishable:

- direct report from the operator
- exact quoted wording
- system interpretation
- hypothesis
- later evidence
- correction
- design principle

Confidence cannot erase class. A later confirmation may promote a hypothesis. The original class stays in history.

### R3. Attempted ≠ completed ≠ verified

A write has three gates:

1. `ATTEMPTED` — the tool call started
2. `COMPLETED` — the tool call returned success
3. `VERIFIED` — the row was read back and matched

Do not claim a save happened at gate 1. If verification is impossible, say so. Do not imply certainty.

### R4. Retrieve the smallest relevant slice

Do not load the whole system by default. The router names the owner for the current task. Open that owner. Stop.

Retrieved is not used. Knowing a row exists does not mean it should fire in this context.

### R5. Recognition does not imply activation

A stored preference, joke, project, or rule applies only when the current context matches its activation conditions. An explicit current instruction can override the default.

### R6. Keep the operator out of bookkeeping

The system infers structure, assigns IDs, routes records, and updates the index. Ask the operator only when a write is high-risk, destructive, or actually ambiguous.

### R7. Deep personal context stays latent

If a system stores sensitive personal records, use them internally only when they change the interpretation of the current task. Do not surface them to prove memory. Do not publish them. They do not belong in this public kit.

### R8. Do not flatten architecture into one prompt

A giant system prompt that recites every table is a failure mode. The model gets `SPEC.md`, the router, and the slice for this task.

## Required surfaces

Every generated system must emit these files:

| File | Owns |
| --- | --- |
| `system_map.csv` | Top-level domains and what they are for |
| `file_index.csv` | Lookup by purpose, not by filename trivia |
| `sources.csv` | Incoming evidence, still not canon |
| `concepts.csv` | Stable ideas with IDs, status, confidence, source links |
| `rules.csv` | Procedural invariants with trigger, action, verification |
| `intake_log.csv` | What got processed, where it went, verification status |
| `router.md` | Which file to open for which kind of task |

Optional later: projects, decisions, telemetry. Do not invent a new truth owner when an existing table already fits.

## Row grammar

Every durable row needs:

- a stable ID (`C-001`, `RULE-003`, `SRC-014`)
- `status` (`ACTIVE`, `DRAFT`, `SUPERSEDED`, `FROZEN`, `REJECTED`)
- `confidence` (`LOW`, `MEDIUM`, `HIGH`) where the row is a claim
- `source_ids` pointing at `sources.csv`
- `notes` only for residue that has no field

Rules also need `trigger`, `action`, and `verification`.

Concepts also need `definition` and `cluster`.

Intake rows also need `routed_to`, `write_status`, and `verified_at`.

## Intake loop

1. Treat incoming text as source evidence, not canon.
2. Preserve wording that matters. Put the raw text in `sources.csv`.
3. Extract durable pieces. Deduplicate against existing IDs.
4. Route each piece to its owner table.
5. Log the route in `intake_log.csv` as `ATTEMPTED`.
6. Read the owner row back.
7. Mark the log `VERIFIED` or `FAILED`.
8. Keep the raw source. Do not delete it to look tidy.

## Status vocabulary

Use these statuses unless the domain has a stronger local list:

- `DRAFT` — written, not trusted
- `ACTIVE` — current and editable
- `SUPERSEDED` — replaced by a newer ID; keep the row
- `FROZEN` — historical snapshot
- `REJECTED` — considered and declined
- `ATTEMPTED` / `COMPLETED` / `VERIFIED` / `FAILED` — write gates only

## What a model may generate

A model may generate a new domain pack from a description: maps, empty or seeded tables, a router, and a first intake example.

A model may propose row edits.

A model may not:

- invent a second editable home for an existing ID
- mark a row `VERIFIED` without a read-back
- promote source wording to a design principle without saying so
- dump private records into the pack
