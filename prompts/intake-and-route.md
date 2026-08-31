# Prompt: intake and route one note

Copy `SPEC.md` and the current owner tables into context. Then paste this.

---

Route the following note through an existing canon-kit pack.

Note:
{{NOTE}}

Rules:

- Add a row to sources.csv. Status DRAFT. Class DIRECT_REPORT unless the note is clearly an interpretation.
- Do not treat the note as canon.
- If it matches an existing concept or rule, link it. Do not mint a duplicate ID.
- If it is new and durable, add at most one concept or one rule.
- Append intake_log.csv with write_status ATTEMPTED, then say exactly which row you will read back.
- After the proposed write, print the exact CSV line you expect to see on read-back.
- Leave write_status as ATTEMPTED in your output. The local script, not the model, flips it to VERIFIED.

Return only the new or changed rows plus the expected read-back line.
