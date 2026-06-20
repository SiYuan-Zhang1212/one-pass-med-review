# Privacy and Storage Policy

The project should treat screenshots as sensitive medical-study material. The core storage rule is:

> Capture continuously, retain selectively.

## What Is Stored Long Term

Long-term records should prefer:

- OCR text.
- Structured answer metadata.
- User outcome: correct, wrong, or unknown.
- Explanation text.
- Short summaries.
- Tags.
- A small number of evidence screenshots only when useful.

## What Is Not Stored Long Term

The app should not store:

- Continuous screen recordings.
- Every periodic screenshot.
- Whole-desktop screenshots by default.
- Raw frames after OCR when they are not needed as evidence.

## Frame Retention Strategy

Recommended runtime behavior:

1. Keep only a small rolling memory buffer, for example the last 5 to 10 seconds.
2. OCR changed frames.
3. Discard raw frame bytes after OCR.
4. Save one or two compressed evidence images only when the user marks a question wrong or requests retention.

## Disk Use Estimate

If every frame is stored, disk use can become hundreds of MB or multiple GB per study session.

With selective retention:

- Correct question: usually a few KB of text and metadata.
- Wrong question: text plus 1 to 2 compressed evidence screenshots.
- Daily usage: usually tens of MB, depending on screenshot retention.

## User Controls

The app should eventually expose:

- Evidence retention duration.
- Whether correct questions can save screenshots.
- Whether AI summarization can use raw OCR text.
- Manual delete for a session or question.
- Export before delete.

## AI Boundary

AI summarization should be optional. When enabled, the app should prefer sending extracted text and user-selected evidence, not full screen recordings.
