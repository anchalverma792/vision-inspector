import cv2
import numpy as np

from .models import ColorResult


def analyze_colors(image: np.ndarray, clusters: int = 5) -> ColorResult:
    """Estimate a compact RGB palette using deterministic k-means."""
    small = cv2.resize(image, (80, 80), interpolation=cv2.INTER_AREA)
    pixels = np.float32(small.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    _, labels, centers = cv2.kmeans(pixels, clusters, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.ravel(), minlength=clusters)
    order = np.argsort(-counts)
    palette = tuple(tuple(int(v) for v in centers[i][::-1]) for i in order)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    colorfulness = float(np.mean(hsv[..., 1]) / 255.0 * 100.0)
    mean_rgb = tuple(int(v) for v in np.mean(rgb, axis=(0, 1)))
    return ColorResult(round(colorfulness, 2), palette, mean_rgb)
