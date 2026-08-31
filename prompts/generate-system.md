# Prompt: generate a canon-kit system

Copy `SPEC.md` into the context first. Then paste this.

---

You are generating a new knowledge system from the canon-kit spec. Emit files, not a speech.

Domain:
{{DOMAIN_DESCRIPTION}}

Constraints:

- Follow SPEC.md exactly.
- Use a fake or operator-supplied domain only. Do not copy anyone's private records.
- Create the required surfaces: system_map.csv, file_index.csv, sources.csv, concepts.csv, rules.csv, intake_log.csv, router.md.
- Seed 5 to 12 real-looking rows per table so a validator has something to chew on.
- Every concept and rule must have an ID, status, and at least one source_id.
- router.md must tell a model which file to open for which job, in under 80 lines.
- Do not write a giant system prompt that restates every row.
- Do not mark any intake row VERIFIED unless you also show the read-back contents.

Output each file in a fenced block with the filename on the first line.

After the files, list:

1. which table is the canonical home for each kind of fact
2. three tasks and the single file the router would open for each
3. one fact you refused to duplicate
