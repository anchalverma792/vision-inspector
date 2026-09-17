import argparse
import json

from .pipeline import analyze_image


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect an image using transparent CV metrics.")
    parser.add_argument("image", help="Path to a PNG/JPEG image")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    report = analyze_image(args.image).to_dict()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['filename']}: {report['width']}x{report['height']}")
        print(f"Quality: {report['quality']['quality_score']}/100")
        print(f"Warnings: {', '.join(report['quality']['warnings']) or 'none'}")
        print(f"Colorfulness: {report['colors']['colorfulness']}% | Edge density: {report['structure']['edge_density']}%")


if __name__ == "__main__":
    main()
