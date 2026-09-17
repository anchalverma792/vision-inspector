import cv2
import numpy as np

from .models import QualityResult


def analyze_quality(image: np.ndarray) -> QualityResult:
    """Compute interpretable exposure, contrast, blur, and warning metrics."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = float(np.mean(gray))
    contrast = float(np.std(gray))
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    warnings: list[str] = []
    if brightness < 45:
        warnings.append("underexposed")
    elif brightness > 210:
        warnings.append("overexposed")
    if contrast < 25:
        warnings.append("low contrast")
    if blur_score < 80:
        warnings.append("possibly blurry")
    exposure_score = max(0.0, 1.0 - abs(brightness - 128.0) / 128.0)
    contrast_score = min(1.0, contrast / 64.0)
    sharpness_score = min(1.0, blur_score / 600.0)
    quality_score = round(100.0 * (0.4 * exposure_score + 0.3 * contrast_score + 0.3 * sharpness_score), 2)
    return QualityResult(round(brightness, 2), round(contrast, 2), round(blur_score, 2), quality_score, tuple(warnings))
