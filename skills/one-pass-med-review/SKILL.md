---
name: one-pass-med-review
description: "Use when Codex needs to operate or improve the One Pass Med Review project: process local medical question practice captures, maintain the SQLite review database, generate concise wrong-question and correct-question reports, or iterate the iPhone-to-Mac screen-capture/OCR workflow."
---

# One Pass Med Review

## Overview

Use this skill to turn one-pass medical question practice sessions into durable review assets. The local Python package is the source of truth; this skill guides Codex in using the repo tools and preserving the privacy/storage constraints.

## Workflow

1. Inspect the repo state before editing.
2. Use the local CLI for storage and report operations:

```bash
onepass init
onepass new-session --title "Session title" --source "iPhone mirrored to Mac"
onepass add-question --session-id 1 --outcome wrong --stem "..." --options-json '["A", "B"]'
onepass report --session-id 1 --output reports/session-1.md
```

3. Keep screenshots selective. Do not design flows that store periodic screenshots permanently.
4. Prefer text and structured metadata in SQLite. Attach evidence screenshots only for wrong questions or explicit user requests.
5. Generate reports that are brief for correct questions and diagnostic for wrong questions.

## Report Style

For wrong questions, include:

- selected answer and correct answer;
- reason the selected answer failed;
- correct reasoning path;
- one discriminating feature or memory hook.

For correct questions, include only:

- one sentence for the core knowledge point;
- optional short tags.

## Engineering Constraints

- Treat OCR output as noisy unless backed by evidence or user confirmation.
- Preserve a local-first workflow. AI summarization must be optional.
- Do not build bulk-copy or redistribution features for proprietary question banks.
- Keep capture/OCR providers swappable.
- Run tests after code changes: `python -m pytest`.

## References

Read `references/reporting.md` when generating or revising study-report wording.
