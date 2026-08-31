# canon-kit

A small, boring kit for building knowledge systems that stay clean.

The point is not a smarter chatbot. The point is structure a model can generate and a script can verify:

- one fact, one canonical home
- attempted is not completed
- completed is not verified
- retrieve the smallest relevant slice
- route messy intake to owners, then read it back

Use it with a local model or a paid API. Paste `SPEC.md` plus a prompt from `prompts/`. The model emits maps and tables. `canonkit` checks that the tables still obey the rules.

This repo is a **sanitized method**. It is not a dump of anyone's private system.

## Quick start

```bash
python -m canonkit validate examples/harbor-lab
python -m canonkit intake examples/harbor-lab "The band saw fence drifts after 20 minutes. Check the rear lock knob."
python -m canonkit validate examples/harbor-lab
```

The intake command writes a source row and an intake-log row, then reads them back. If the read-back fails, it does not claim success.

## What you get

| Piece | Job |
| --- | --- |
| `SPEC.md` | The rules. Give this to a model. |
| `prompts/` | Prompts that emit a new system from a domain description. |
| `schema/canonkit.sql` | SQLite shape of the same rules. |
| `examples/harbor-lab/` | A fake workshop used as the working sample. |
| `canonkit/` | Validator and intake router. |

## What this is not

- Not a persona pack
- Not a memory that updates model weights
- Not permission to flatten a whole private architecture into one system prompt
- Not a source of truth for any real person, family, medical, or identity record

Facts, projects, and provenance stay in tables. The model only sees the slice the router hands it.

## License

MIT
