from dataclasses import dataclass, field
from time import time


BBox = tuple[int, int, int, int]


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    bbox: BBox

    @property
    def center_x(self) -> float:
        x1, _, x2, _ = self.bbox
        return (x1 + x2) / 2


@dataclass(frozen=True)
class FindResult:
    label: str
    found: bool
    region: str | None = None
    confidence: float | None = None
    bbox: BBox | None = None


@dataclass
class SceneState:
    detections: list[Detection] = field(default_factory=list)
    frame_width: int = 640
    updated_at: float = field(default_factory=time)

    def list_objects(self) -> list[str]:
        best: dict[str, float] = {}
        for detection in self.detections:
            best[detection.label] = max(best.get(detection.label, 0.0), detection.confidence)
        return [label for label, _ in sorted(best.items(), key=lambda item: item[1], reverse=True)]

    def find(self, label: str) -> FindResult:
        matches = [item for item in self.detections if item.label == label]
        if not matches:
            return FindResult(label=label, found=False)

        best = max(matches, key=lambda item: item.confidence)
        return FindResult(
            label=label,
            found=True,
            region=self._region_for(best),
            confidence=best.confidence,
            bbox=best.bbox,
        )

    def has_any(self, labels: set[str]) -> bool:
        return any(item.label in labels for item in self.detections)

    def _region_for(self, detection: Detection) -> str:
        third = self.frame_width / 3
        if detection.center_x < third:
            return "left"
        if detection.center_x < third * 2:
            return "center"
        return "right"
