from __future__ import annotations

import subprocess
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from .hashing import file_sha256
from .models import utc_now


@dataclass(frozen=True, slots=True)
class CaptureRegion:
    x: int
    y: int
    width: int
    height: int

    @classmethod
    def parse(cls, value: str) -> "CaptureRegion":
        parts = [part.strip() for part in value.split(",")]
        if len(parts) != 4:
            raise ValueError("region must be x,y,width,height")
        x, y, width, height = (int(part) for part in parts)
        if width <= 0 or height <= 0:
            raise ValueError("region width and height must be positive")
        return cls(x=x, y=y, width=width, height=height)

    def to_screencapture_arg(self) -> str:
        return f"{self.x},{self.y},{self.width},{self.height}"


class MacScreenCapture:
    """Thin wrapper around macOS screencapture for the selected region."""

    def __init__(self, region: CaptureRegion | None = None) -> None:
        self.region = region

    def capture_to(self, output_path: str | Path) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        command = ["screencapture", "-x"]
        if self.region is not None:
            command.extend(["-R", self.region.to_screencapture_arg()])
        command.append(str(path))
        subprocess.run(command, check=True)
        return file_sha256(str(path))


@dataclass(frozen=True, slots=True)
class FrameSnapshot:
    captured_at: str
    sha256: str
    data: bytes


class RollingFrameBuffer:
    """In-memory frame buffer so routine screenshots do not hit disk."""

    def __init__(self, max_frames: int = 10) -> None:
        if max_frames <= 0:
            raise ValueError("max_frames must be positive")
        self._frames: deque[FrameSnapshot] = deque(maxlen=max_frames)

    def add(self, data: bytes, sha256: str) -> None:
        self._frames.append(FrameSnapshot(captured_at=utc_now(), sha256=sha256, data=data))

    def latest(self) -> FrameSnapshot | None:
        if not self._frames:
            return None
        return self._frames[-1]

    def all(self) -> list[FrameSnapshot]:
        return list(self._frames)
