import cv2
import numpy as np

from .models import StructureResult


def analyze_structure(image: np.ndarray) -> StructureResult:
    """Summarize edges, contours, and foreground-like connected regions."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(np.count_nonzero(edges) / edges.size * 100.0)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area = image.shape[0] * image.shape[1]
    largest = max((cv2.contourArea(c) for c in contours), default=0.0) / area
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    components = cv2.connectedComponents(binary)[0] - 1
    return StructureResult(round(edge_density, 2), len(contours), round(float(largest), 4), int(max(0, components)))
