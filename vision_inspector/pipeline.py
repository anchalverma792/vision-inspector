from pathlib import Path

import cv2

from .colors import analyze_colors
from .models import InspectionReport
from .quality import analyze_quality
from .structure import analyze_structure


def analyze_image(path: str | Path) -> InspectionReport:
    """Load one local image and run all inspection modules."""
    source = Path(path)
    if not source.exists() or not source.is_file():
        raise ValueError(f"Could not read a supported image: {source}")
    image = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read a supported image: {source}")
    height, width, channels = image.shape
    return InspectionReport(source.name, width, height, channels, analyze_quality(image), analyze_colors(image), analyze_structure(image))
