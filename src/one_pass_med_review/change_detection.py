from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FrameDigest:
    sha256: str


def should_process_frame(previous: FrameDigest | None, current: FrameDigest) -> bool:
    if previous is None:
        return True
    return previous.sha256 != current.sha256
