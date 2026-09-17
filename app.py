from pathlib import Path
import tempfile

import cv2
import numpy as np
import streamlit as st

from vision_inspector.pipeline import analyze_image

st.set_page_config(page_title="Vision Inspector", page_icon="🔎", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2rem;}
.hero {padding: 1.3rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#0f766e,#155e75); color: white; margin-bottom: 1.2rem;}
.hero h1 {margin: 0; font-size: 2.2rem;}.hero p {margin: .35rem 0 0; opacity: .9;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🔎 Vision Inspector</h1><p>Transparent, local-first computer-vision triage for image datasets.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Inspection workflow")
    st.write("1. Upload an image\n2. Review quality warnings\n3. Explore color and structure metrics\n4. Export the report as JSON")
    st.caption("All processing happens locally. No image is sent to an external service.")

uploaded = st.file_uploader("Upload a PNG or JPEG image", type=["png", "jpg", "jpeg"])
if not uploaded:
    st.info("Upload an image to begin the inspection.")
    st.markdown("#### What this tool measures")
    st.write("Image quality · dominant colors · edges and contours · connected regions")
    st.stop()

try:
    suffix = Path(uploaded.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as handle:
        handle.write(uploaded.getbuffer())
        image_path = handle.name
    report = analyze_image(image_path)
except (OSError, ValueError) as exc:
    st.error(f"Inspection failed: {exc}")
    st.stop()

left, right = st.columns([1.15, 1])
with left:
    st.image(uploaded, caption=f"Input image: {uploaded.name}", use_container_width=True)
with right:
    st.subheader("Inspection summary")
    a, b, c = st.columns(3)
    a.metric("Quality", f"{report.quality.quality_score}/100")
    b.metric("Brightness", f"{report.quality.brightness}")
    c.metric("Edge density", f"{report.structure.edge_density}%")
    if report.quality.warnings:
        st.warning("Warnings: " + ", ".join(report.quality.warnings))
    else:
        st.success("No quality warnings detected.")
    st.download_button("Download JSON report", report.to_json(), f"{Path(uploaded.name).stem}_inspection.json", "application/json")

quality_tab, color_tab, structure_tab = st.tabs(["1 · Quality analysis", "2 · Color analysis", "3 · Structure analysis"])
with quality_tab:
    st.subheader("Quality analysis")
    st.caption("Grayscale statistics and Laplacian variance create an explainable first-pass quality score.")
    st.dataframe({"Metric": ["Brightness", "Contrast", "Blur score", "Quality score"], "Value": [report.quality.brightness, report.quality.contrast, report.quality.blur_score, report.quality.quality_score]}, hide_index=True, use_container_width=True)
    st.progress(int(report.quality.quality_score), text="Heuristic quality score")
with color_tab:
    st.subheader("Color analysis")
    st.caption("HSV saturation estimates colorfulness; deterministic k-means summarizes the dominant RGB palette.")
    st.metric("Colorfulness", f"{report.colors.colorfulness}%")
    st.write(f"Mean RGB: {report.colors.mean_rgb}")
    palette = np.array([color for color in report.colors.dominant_colors], dtype=np.uint8).reshape(1, -1, 3)
    st.image(cv2.cvtColor(palette, cv2.COLOR_RGB2BGR), caption="Dominant colors, ordered by frequency", use_container_width=True)
    st.write({"Dominant RGB colors": report.colors.dominant_colors})
with structure_tab:
    st.subheader("Structure analysis")
    st.caption("Canny edges, external contours, Otsu thresholding, and connected components describe visual structure.")
    st.dataframe({"Metric": ["Edge density", "External contours", "Largest contour ratio", "Connected components"], "Value": [f"{report.structure.edge_density}%", report.structure.contour_count, report.structure.largest_contour_ratio, report.structure.connected_components]}, hide_index=True, use_container_width=True)
