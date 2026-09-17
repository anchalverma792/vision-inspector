import cv2
import numpy as np
import pytest

from vision_inspector.pipeline import analyze_image


def test_pipeline_returns_bounded_metrics(tmp_path):
    image = np.zeros((80, 120, 3), dtype=np.uint8)
    image[:, :60] = (255, 40, 20)
    image[:, 60:] = (20, 40, 255)
    path = tmp_path / "fixture.png"
    assert cv2.imwrite(str(path), image)
    report = analyze_image(path)
    assert (report.width, report.height, report.channels) == (120, 80, 3)
    assert 0 <= report.quality.quality_score <= 100
    assert 0 <= report.colors.colorfulness <= 100
    assert report.structure.edge_density >= 0


def test_invalid_file_has_actionable_error(tmp_path):
    path = tmp_path / "not-image.txt"
    path.write_text("not an image", encoding="utf-8")
    with pytest.raises(ValueError, match="supported image"):
        analyze_image(path)


def test_json_contract_contains_all_modules(tmp_path):
    image = np.full((30, 30, 3), 120, dtype=np.uint8)
    path = tmp_path / "fixture.jpg"
    assert cv2.imwrite(str(path), image)
    payload = analyze_image(path).to_dict()
    assert set(payload) == {"filename", "width", "height", "channels", "quality", "colors", "structure"}
    assert "warnings" in payload["quality"]


def test_missing_path_has_actionable_error(tmp_path):
    with pytest.raises(ValueError, match="supported image"):
        analyze_image(tmp_path / "missing.png")
