from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Vision_Inspector_Project_Report.pdf"


def box(title: str, body: str):
    table = Table([[Paragraph(f"<b>{title}</b>", styles["BodyText"]), Paragraph(body, styles["BodyText"])]], colWidths=[1.55 * inch, 4.9 * inch])
    table.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#334155")), ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#e2e8f0")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 8)]))
    return table


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=30, leading=36, alignment=TA_CENTER, textColor=colors.HexColor("#0f172a"), spaceAfter=18))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=14, alignment=TA_CENTER, textColor=colors.HexColor("#475569"), spaceAfter=30))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontSize=19, leading=23, textColor=colors.HexColor("#0f766e"), spaceBefore=8, spaceAfter=10))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11))


def bullets(items):
    return [Paragraph(f"• {item}", styles["BodyText"]) for item in items]


story = [Spacer(1, 1.3 * inch), Paragraph("Vision Inspector", styles["CoverTitle"]), Paragraph("A transparent computer-vision image inspection dashboard", styles["CoverSub"]), Spacer(1, 1.5 * inch), box("Course", "Computer Vision"), Spacer(1, 12), box("Submission", "VITyarthi Build Your Own Project"), Spacer(1, 12), box("Version", "1.0.0"), PageBreak()]
story += [Paragraph("1. Introduction", styles["Section"]), Paragraph("Vision Inspector is a local-first tool that turns an image into a compact, interpretable inspection report. It applies classical computer-vision operations so students and dataset curators can understand why an image may need review without relying on an opaque model or external API.", styles["BodyText"]), Spacer(1, 8), Paragraph("2. Problem Statement", styles["Section"]), Paragraph("Image collections commonly contain exposure problems, blur, weak contrast, repetitive colors, or insufficient structure. Manual review is slow and subjective. The proposed system provides a repeatable first-pass audit while leaving the final retain/correct/review decision to a human.", styles["BodyText"]), Paragraph("Objectives", styles["Heading2"])] + bullets(["Apply image statistics, color-space conversion, clustering, edge detection, contour extraction, and connected components.", "Deliver three major functional modules with clear input/output contracts.", "Provide both an interactive dashboard and a JSON-capable CLI.", "Document the design and validate it with automated tests."])
story += [Paragraph("3. Functional Requirements", styles["Section"]), box("FR-1 Quality", "Calculate brightness, contrast, Laplacian blur score, a 0–100 heuristic quality score, and warnings."), Spacer(1, 6), box("FR-2 Color", "Estimate colorfulness, mean RGB, and the dominant RGB palette using deterministic k-means."), Spacer(1, 6), box("FR-3 Structure", "Calculate Canny edge density, external contour count, largest contour ratio, and connected components."), Spacer(1, 6), box("FR-4 Output", "Show human-readable findings in Streamlit and serialize the complete report as JSON from the CLI."), Paragraph("4. Non-functional Requirements", styles["Section"])] + bullets(["Performance: downsample color clustering to 80×80; avoid unnecessary full-resolution operations.", "Security: process uploaded images locally; never transmit them to a third party.", "Usability: provide plain-language warnings and a one-command CLI path.", "Reliability: reject unreadable files with an actionable ValueError.", "Maintainability: keep modules single-purpose and expose typed dataclass results.", "Resource efficiency: use bounded palette samples and no persistent database."])
story += [PageBreak(), Paragraph("5. System Architecture", styles["Section"]), Paragraph("The architecture separates presentation, orchestration, domain algorithms, and result contracts.", styles["BodyText"]), Spacer(1, 10), box("User", "Uploads a PNG/JPEG in the dashboard or supplies a local path to the CLI."), Spacer(1, 6), box("App / CLI", "Accepts input and requests one analysis through the pipeline."), Spacer(1, 6), box("Pipeline", "Loads and validates the image, then invokes quality, color, and structure modules."), Spacer(1, 6), box("Analysis modules", "OpenCV and NumPy algorithms return typed, serializable result objects."), Spacer(1, 6), box("Report", "Dashboard cards or JSON output provide findings and measurements."), Paragraph("6. Design Diagrams", styles["Section"]), Paragraph("Workflow: Input image → Load/validate → Quality + Color + Structure (parallel conceptual modules) → Combine report → Display/export.", styles["BodyText"]), Spacer(1, 8), Paragraph("Use cases", styles["Heading2"])] + bullets(["Dataset curator: upload image, inspect warnings, decide whether to review.", "Developer: run CLI with --json, pipe metrics into another tool.", "Student: read each metric and connect it to a classical CV operation."]) + [Paragraph("Component design", styles["Heading2"]), Paragraph("The pipeline depends on three pure analysis modules. Each returns a dataclass defined in models.py. The UI and CLI depend on the pipeline, not on OpenCV details. This dependency direction makes algorithms testable without the interface.", styles["BodyText"]), Paragraph("Storage design", styles["Heading2"]), Paragraph("No persistent storage is used. The source image remains at its original location; the report exists in memory and can be serialized to stdout. This reduces privacy risk and keeps the project portable.", styles["BodyText"])]
story += [Paragraph("7. Implementation Details", styles["Section"]), Paragraph("Quality uses grayscale mean/std statistics and Laplacian variance. Color analysis converts BGR to HSV for saturation-based colorfulness and uses deterministic OpenCV k-means on a bounded thumbnail. Structure analysis uses Canny edges, external contours, Otsu thresholding, and connected components. The Streamlit app creates a temporary local copy only for the duration of an inspection.", styles["BodyText"]), Paragraph("8. Testing Approach", styles["Section"]), Paragraph("The test suite writes a synthetic two-color fixture, checks dimensions and bounded metric ranges, and verifies an invalid file produces an actionable error. The design supports further fixture-based tests for dark, bright, and blurry images.", styles["BodyText"]), Spacer(1, 8), Table([["Test", "Expected result"], ["Synthetic valid PNG", "Report dimensions and metrics are valid"], ["Unreadable text file", "ValueError includes supported image"], ["CLI --json", "Valid JSON report on stdout"]], colWidths=[2.2 * inch, 4.25 * inch], style=TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ccfbf1")), ("PADDING", (0, 0), (-1, -1), 6)])), Paragraph("9. Challenges Faced", styles["Section"]), Paragraph("The main design challenge was balancing useful signals with explainability. A single score can hide the cause of a problem, so the project reports both the score and its component metrics. Another challenge was keeping execution deterministic and lightweight; bounded sampling and fixed clustering criteria address this.", styles["BodyText"]), Paragraph("10. Learnings and Key Takeaways", styles["Section"])] + bullets(["Classical CV primitives can produce useful dataset triage signals without model training.", "Typed boundaries make it easier to reuse the same analysis from a UI and a CLI.", "Human-readable warnings are most useful when paired with the underlying measurement.\n"]) + [Paragraph("11. Future Enhancements", styles["Section"])] + bullets(["Batch directory analysis with CSV/JSONL export.", "Optional perceptual-hash duplicate detection.", "Configurable thresholds and saved inspection profiles.", "Interactive plots and side-by-side before/after enhancement previews."]) + [Paragraph("12. References", styles["Section"]), Paragraph("OpenCV documentation: image processing, color conversion, k-means, Canny, contours, and connected components. NumPy documentation: array statistics and reshaping. Streamlit documentation: file upload and metric components.", styles["BodyText"])]


story += [PageBreak(), Paragraph("13. Screenshots / Results", styles["Section"]), Paragraph("Runtime verification was performed against the Streamlit dashboard using the generated sample_scene.png. The working dashboard displayed the uploaded image, quality score 73.83/100, brightness 158.08, edge density 1.36%, colorfulness 48.95%, and a no-warning success state. The three module tabs rendered quality, color palette, and structure outputs. Runtime captures are documented in the submission notes and should be saved into docs/screenshots before portal upload if local screenshot export is required.", styles["BodyText"]), Spacer(1, 10), Paragraph("14. Manual submission fields", styles["Section"]), Paragraph("Student name, roll number, faculty, semester, and academic year were not supplied and remain intentionally absent from this generic Computer Vision report cover page.", styles["BodyText"])]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(0.7 * inch, 0.45 * inch, "Vision Inspector | VITyarthi Project Report")
    canvas.drawRightString(7.8 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


OUT.parent.mkdir(exist_ok=True)
SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=0.7 * inch, leftMargin=0.7 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch, title="Vision Inspector Project Report").build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
