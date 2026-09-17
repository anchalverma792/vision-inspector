# Design Decisions

- Classical CV was selected because it is transparent, lightweight, and easy to demonstrate without model downloads.
- A pipeline boundary keeps UI/CLI code independent from algorithm details.
- Dataclasses provide an explicit input/output contract and predictable JSON export.
- No database is used because one-image inspection does not need persistence and local-only processing improves privacy.
- The quality score is explicitly heuristic; underlying metrics and warnings remain visible.
