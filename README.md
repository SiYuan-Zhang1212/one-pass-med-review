# One Pass Med Review

One Pass Med Review is a local-first study assistant for medical question practice. The goal is simple: do each question once, capture the learning value, and avoid wasting review time by repeatedly browsing the same question bank.

The project is designed for a Mac workflow where an iPhone screen is mirrored to the desktop, a local tool observes the mirrored question area, OCR extracts the visible content, and the app turns correct and wrong attempts into concise review assets.

## Status

This repository is at MVP scaffold stage.

Implemented now:

- SQLite storage for practice sessions, question records, and optional evidence screenshots.
- CLI commands to initialize storage, create sessions, add question records, and generate Markdown reports.
- A storage policy that avoids retaining continuous screenshots.
- A repo-contained Codex skill draft for future AI-assisted report processing.
- Basic tests and GitHub Actions CI.

Planned next:

- Window/region selection for the mirrored iPhone screen.
- OCR provider integrations.
- Hotkeys for "correct", "wrong", and "question finished".
- Optional AI summarization with local-first redaction controls.
- Anki and CSV export.

## Design Principles

- Local-first by default.
- Do not store a continuous recording.
- OCR frames are temporary inputs, not permanent data.
- Save screenshots only when they are useful evidence, especially for wrong questions.
- Keep summaries short for correct questions and more diagnostic for wrong questions.
- Make every automation step auditable before trusting it.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

onepass init
onepass demo
```

Create a real session:

```bash
onepass new-session --title "医考帮第一轮 - 呼吸系统" --source "iPhone mirrored to Mac"
```

Add a question manually while the capture/OCR layer is still being built:

```bash
onepass add-question \
  --session-id 1 \
  --outcome wrong \
  --stem "患者咳嗽、咳痰伴发热，胸片提示..." \
  --options-json '["肺炎链球菌肺炎", "肺结核", "支气管哮喘"]' \
  --selected-answer "肺结核" \
  --correct-answer "肺炎链球菌肺炎" \
  --explanation "典型表现和影像更符合肺炎链球菌肺炎。" \
  --summary "错因：把急性感染性表现误判为慢性病程。复习：肺炎链球菌肺炎常见铁锈色痰和大叶实变。"
```

Generate a Markdown report:

```bash
onepass report --session-id 1 --output reports/session-1.md
```

## Repository Layout

```text
.
├── docs/                         # Architecture and product notes
├── skills/one-pass-med-review/   # Repo-contained Codex skill draft
├── src/one_pass_med_review/      # Python package
├── tests/                        # Pytest suite
├── pyproject.toml
└── README.md
```

## Privacy and Storage

The intended production loop is:

1. Capture the mirrored iPhone region.
2. Detect whether the frame meaningfully changed.
3. Run OCR.
4. Discard the raw frame unless a rule or hotkey marks it as evidence.
5. Store text, structured metadata, short summaries, and selected evidence only.

See [docs/privacy-and-storage.md](docs/privacy-and-storage.md) for the full policy.

## Legal and Platform Boundaries

This project is intended for personal study workflows. It should not be used to bulk copy, redistribute, or republish proprietary question bank content. The safest long-term artifact is a personal knowledge summary, not a mirrored copy of the source material.

## GitHub Publishing

This local repo does not yet have a GitHub remote configured. See [docs/github-publishing.md](docs/github-publishing.md) for the exact publish commands once a GitHub repository exists.

## License

MIT. See [LICENSE](LICENSE).
