from pathlib import Path
import tempfile

import cv2
import numpy as np
import streamlit as st

from vision_inspector.pipeline import analyze_image

st.set_page_config(page_title="Vision Inspector", page_icon="🔎", layout="wide")

st.markdown("""
<style>
.stApp {background: #f6f8fb;}
.block-container {max-width: 1220px; padding: 2.2rem 2.2rem 4rem;}
[data-testid="stSidebar"] {background: #0b1324;}
[data-testid="stSidebar"] * {color: #e2e8f0 !important;}
[data-testid="stSidebar"] hr {border-color: #25324a;}
.hero {padding: 1.65rem 1.9rem; border-radius: 22px; background: linear-gradient(120deg,#0b1324 0%,#123b56 52%,#0f766e 100%); color: white; margin-bottom: 1.5rem; box-shadow: 0 16px 38px rgba(15,23,42,.14);}
.hero h1 {margin: 0; font-size: 2.45rem; letter-spacing: -.04em;}.hero p {margin: .5rem 0 0; color: #c8d8e8; font-size: 1.02rem;}
.eyebrow {font-size: .76rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #8fe3d2; margin-bottom: .55rem;}
.section-label {font-size: .78rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; color: #0f766e; margin: 1.1rem 0 .55rem;}
.detail-label {font-size: .86rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: #7c3aed; margin: 1.35rem 0 .7rem;}
.module-card {background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1rem 1.1rem; height: 100%; box-shadow: 0 5px 16px rgba(15,23,42,.05);}
.module-card h4 {margin: 0 0 .35rem; color: #0f172a;}.module-card p {margin: 0; color: #64748b; font-size: .88rem; line-height: 1.45;}
.metric-strip {background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: .45rem .7rem; box-shadow: 0 5px 16px rgba(15,23,42,.04);}
.stTabs [data-baseweb="tab-list"] {gap: .45rem; background: white; padding: .4rem; border: 1px solid #e2e8f0; border-radius: 14px;}
.stTabs [data-baseweb="tab"] {height: 2.7rem; border-radius: 10px; padding: 0 1rem;}
.stTabs [aria-selected="true"] {background: #dff7f1; color: #0f766e;}
.stButton button, .stDownloadButton button {border-radius: 10px; font-weight: 650;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">Computer Vision Lab · VITyarthi Project</div><h1>🔎 Vision Inspector</h1><p>Turn one image into a clear, explainable inspection report.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔎 Vision Inspector")
    st.caption("LOCAL-FIRST IMAGE AUDIT")
    st.divider()
    st.markdown("### Inspection workflow")
    st.markdown("**01**  Upload an image  \n**02**  Review quality warnings  \n**03**  Explore color and structure  \n**04**  Export the JSON report")
    st.divider()
    st.markdown("### Analysis modules")
    st.markdown("Quality · Color · Structure")
    st.caption("Privacy note: all processing happens locally. No image is sent to an external service.")

uploaded = st.file_uploader("Upload a PNG or JPEG image", type=["png", "jpg", "jpeg"])
if not uploaded:
    st.markdown('<div class="section-label">Start here</div>', unsafe_allow_html=True)
    st.info("Upload an image to begin the inspection.")
    st.markdown('<div class="section-label">What this tool measures</div>', unsafe_allow_html=True)
    modules = st.columns(3)
    cards = [("01 · Quality", "Brightness, contrast, blur score, and actionable warnings."), ("02 · Color", "Colorfulness, mean RGB, and dominant palette."), ("03 · Structure", "Edges, contours, and connected visual regions.")]
    for column, (title, body) in zip(modules, cards):
        with column:
            st.markdown(f'<div class="module-card"><h4>{title}</h4><p>{body}</p></div>', unsafe_allow_html=True)
    st.stop()

try:
    suffix = Path(uploaded.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as handle:
        handle.write(uploaded.getbuffer())
        image_path = handle.name
    with st.spinner("Running quality, color, and structure analysis..."):
        report = analyze_image(image_path)
except (OSError, ValueError) as exc:
    st.error(f"Inspection failed: {exc}")
    st.stop()

st.markdown('<div class="section-label">Inspection overview</div>', unsafe_allow_html=True)
left, right = st.columns([1.08, 1])
with left:
    st.image(uploaded, caption=f"Input image: {uploaded.name}", use_container_width=True)
with right:
    st.markdown('<div class="metric-strip">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="detail-label">Detailed analysis</div>', unsafe_allow_html=True)
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
