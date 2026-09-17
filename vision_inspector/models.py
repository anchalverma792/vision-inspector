from dataclasses import asdict, dataclass
import json
from typing import Any


@dataclass(frozen=True)
class QualityResult:
    brightness: float
    contrast: float
    blur_score: float
    quality_score: float
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class ColorResult:
    colorfulness: float
    dominant_colors: tuple[tuple[int, int, int], ...]
    mean_rgb: tuple[int, int, int]


@dataclass(frozen=True)
class StructureResult:
    edge_density: float
    contour_count: int
    largest_contour_ratio: float
    connected_components: int


@dataclass(frozen=True)
class InspectionReport:
    filename: str
    width: int
    height: int
    channels: int
    quality: QualityResult
    colors: ColorResult
    structure: StructureResult

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        """Serialize the report for download or command-line integrations."""
        return json.dumps(self.to_dict(), indent=2)
