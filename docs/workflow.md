# Workflow

The user supplies one PNG/JPEG. The pipeline checks that the path exists and OpenCV can decode it. Quality, color, and structure analyses run, their typed outputs are assembled, and the user reviews the dashboard or downloads JSON. Invalid input produces an error state and no report.

See `diagrams/workflow.mmd` and `diagrams/sequence.mmd`.
