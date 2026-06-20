# Roadmap

## Phase 0: Repository Baseline

- Create open-source repo structure.
- Add local SQLite model.
- Add manual CLI workflow.
- Add documentation for architecture and storage.
- Add CI.

## Phase 1: Manual MVP

- Start a study session.
- Use hotkeys to mark correct and wrong questions.
- Store OCR text and optional screenshots.
- Generate Markdown reports.
- Add CSV export.

## Phase 2: Capture and OCR

- Select mirrored iPhone region.
- Capture frames from that region only.
- Add change detection.
- Integrate the first OCR provider.
- Persist OCR text without retaining every raw frame.

## Phase 3: Question Flow Automation

- Detect question boundaries.
- Detect answer submission and explanation screen.
- Deduplicate repeated questions by normalized hash.
- Auto-attach evidence screenshots for wrong questions.

## Phase 4: Review Intelligence

- Generate wrong-question diagnosis.
- Generate one-line correct-question summaries.
- Tag by system, subject, and knowledge point.
- Export Anki cards.

## Phase 5: Mac App

- Menu bar app.
- Region picker.
- Capture status indicator.
- Hotkey settings.
- Review dashboard.
