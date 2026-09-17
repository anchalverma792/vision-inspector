# Project Statement - Vision Inspector

## Problem statement

Image datasets often contain dark, overexposed, blurry, or visually repetitive images. Finding those issues manually is slow and inconsistent. Vision Inspector provides a transparent pre-processing inspection step that explains measurable image properties before a human decides whether an image should be retained, corrected, or reviewed.

## Objectives

- Build an original computer-vision application using classical image-processing concepts.
- Provide three major functional modules: quality, color, and structure analysis.
- Expose clear input/output contracts through a reusable Python pipeline and CLI.
- Produce documentation, diagrams, validation, and automated tests suitable for a GitHub submission.

## Scope

In scope: PNG/JPEG image loading, grayscale statistics, Laplacian blur estimation, HSV colorfulness, dominant-color extraction, Canny edge density, contour summaries, a combined report, JSON export, and a Streamlit dashboard.

Out of scope: object identity recognition, face recognition, cloud storage, model training, and automatic deletion or modification of source images.

## Target users

- Students learning computer vision fundamentals.
- Dataset curators performing a first-pass image audit.
- Developers debugging image capture pipelines.

## High-level features

- Local-only image analysis.
- Human-readable dashboard and machine-readable JSON output.
- Interpretable metrics and warnings.
- Deterministic analysis for the same image and configuration.
- Tests for loading, metric ranges, and error handling.
