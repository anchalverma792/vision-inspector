# System Architecture

Vision Inspector uses a small layered architecture. The Streamlit UI and CLI are adapters. Both call the pipeline, which validates the input and coordinates the three domain modules. The modules use OpenCV/NumPy and return typed result objects. The final `InspectionReport` is rendered as UI metrics or serialized JSON.

See `diagrams/architecture.mmd` and `diagrams/component.mmd`.
