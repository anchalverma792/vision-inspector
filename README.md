# Vision Inspector

Vision Inspector is a modular computer-vision tool for quickly understanding an image before a model is trained or a dataset is published. It combines three functional modules in one workflow:

1. **Quality analysis** - brightness, contrast, blur, exposure, and a quality score.
2. **Color analysis** - dominant colors, colorfulness, and a compact palette.
3. **Structure analysis** - edge density, connected components, and contour statistics.

The project is deliberately self-contained: it uses classical computer-vision techniques (OpenCV and NumPy), so it runs without downloading a machine-learning model or sending images to a service.

## Run

```powershell
cd vision_inspector
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\make_demo_image.py
python -m vision_inspector.cli data\sample_scene.png --json
```

To run the interactive dashboard:

```powershell
streamlit run app.py
```

## Test

```powershell
pytest -q
```

## Architecture and academic artifacts

Inputs are one PNG/JPEG image. Streamlit or the CLI calls the pipeline, which validates the image and coordinates quality, color, and structure modules. A typed `InspectionReport` is rendered as dashboard metrics or JSON. See `docs/architecture.md` and `docs/diagrams/`.

The detailed report is `docs/Vision_Inspector_Project_Report.pdf`; the requirement audit is `docs/FINAL_CHECKLIST.md`. Design notes, workflow, testing, and references are in `docs/`.

## Project structure

```text
vision_inspector/
  app.py                    Streamlit user interface
  statement.md              Problem statement and scope
  requirements.txt          Runtime and test dependencies
  vision_inspector/
    __init__.py
    cli.py                   Command-line entry point
    models.py                Typed result contracts
    pipeline.py              Orchestrates the analysis modules
    quality.py               Image quality metrics
    colors.py                Palette and color metrics
    structure.py             Edge and contour metrics
  tests/
    test_pipeline.py
```

## Notes

The quality score is a heuristic, not a medical, security, or production acceptance decision. Use the per-metric values to investigate borderline images. Supported inputs are common Pillow/OpenCV formats such as PNG and JPEG.
