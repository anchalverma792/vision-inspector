# Requirements

## Functional requirements

- FR-1: accept a PNG or JPEG through the dashboard or CLI.
- FR-2: validate and decode the image; show an actionable error for invalid input.
- FR-3: compute quality metrics and human-readable warnings.
- FR-4: compute colorfulness, mean RGB, and dominant colors.
- FR-5: compute edge, contour, and connected-component structure metrics.
- FR-6: present the complete result in the dashboard and export JSON.

## Non-functional requirements

- NFR-1 Performance: color clustering uses an 80×80 thumbnail.
- NFR-2 Security/privacy: processing is local; no network service or credential is required.
- NFR-3 Usability: plain-language labels, tabs, success, warning, and error states.
- NFR-4 Reliability: invalid paths and unreadable files fail with a clear `ValueError`.
- NFR-5 Maintainability: each CV module has a single responsibility and typed dataclass output.
- NFR-6 Resource efficiency: no persistent database; analysis results are bounded in memory.
