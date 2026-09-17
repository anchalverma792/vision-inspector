"""Create a deterministic demo image for classroom demonstrations."""
from pathlib import Path
import cv2
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "data" / "sample_scene.png"
image = np.full((480, 720, 3), (235, 220, 190), dtype=np.uint8)
cv2.rectangle(image, (45, 55), (675, 425), (55, 110, 150), -1)
cv2.circle(image, (180, 210), 95, (40, 180, 220), -1)
cv2.circle(image, (520, 290), 110, (70, 190, 90), -1)
cv2.line(image, (80, 370), (640, 85), (245, 245, 245), 12)
cv2.putText(image, "CV DATASET", (205, 125), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (20, 35, 50), 3, cv2.LINE_AA)
OUT.parent.mkdir(parents=True, exist_ok=True)
cv2.imwrite(str(OUT), image)
print(OUT)
