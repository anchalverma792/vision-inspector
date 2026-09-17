# Implementation

Quality analysis converts BGR to grayscale, then uses mean, standard deviation, and Laplacian variance. Color analysis converts to HSV for saturation-based colorfulness and applies deterministic OpenCV k-means to a bounded thumbnail. Structure analysis uses Canny, external contours, Otsu thresholding, and connected components. The Streamlit app writes the upload to a temporary local file, invokes the same pipeline as the CLI, and exposes JSON download.
