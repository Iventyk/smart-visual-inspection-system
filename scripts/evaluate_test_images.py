"""Evaluate bundled test images and print CV summary metrics."""

import argparse
import json
from pathlib import Path

from app.cv.pipeline import analyze_image_bytes


def _format_categories(categories: list[str]) -> str:
    return ", ".join(categories) if categories else "—"


def evaluate_images(image_dir: Path) -> list[dict]:
    """Run the CV pipeline for each image in a directory."""
    image_paths = sorted(
        path
        for path in image_dir.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    rows = []
    for path in image_paths:
        result_json, _ = analyze_image_bytes(path.read_bytes())
        result = json.loads(result_json)
        summary = result["results"]["summary"]
        rows.append(
            {
                "image": path.name,
                "detections": summary["total_detections"],
                "accuracy_percent": summary["detection_accuracy_percent"],
                "category_count": summary["detected_category_count"],
                "categories": summary["detected_categories"],
                "processing_time_ms": summary["processing_time_ms"],
                "throughput_images_per_min": summary[
                    "throughput_images_per_min"
                ],
            }
        )
    return rows


def print_markdown(rows: list[dict]) -> None:
    """Print a Markdown table and aggregate metrics."""
    print(
        "| Image | Detections | Accuracy (%) | Categories | "
        "Processing (ms) | Throughput (images/min) |"
    )
    print("| --- | ---: | ---: | --- | ---: | ---: |")
    for row in rows:
        print(
            f"| `{row['image']}` | {row['detections']} | "
            f"{row['accuracy_percent']:.2f} | "
            f"{row['category_count']} ({_format_categories(row['categories'])}) | "
            f"{row['processing_time_ms']} | "
            f"{row['throughput_images_per_min']:.2f} |"
        )

    if not rows:
        return

    all_categories = sorted(
        {category for row in rows for category in row["categories"]}
    )
    avg_accuracy = sum(row["accuracy_percent"] for row in rows) / len(rows)
    avg_processing_ms = sum(row["processing_time_ms"] for row in rows) / len(
        rows
    )
    avg_throughput = sum(
        row["throughput_images_per_min"] for row in rows
    ) / len(rows)
    total_detections = sum(row["detections"] for row in rows)

    print()
    print(f"- Images evaluated: {len(rows)}")
    print(f"- Total detections: {total_detections}")
    print(f"- Unique detected categories: {len(all_categories)}")
    print(f"- Category names: {_format_categories(all_categories)}")
    print(f"- Mean detection accuracy: {avg_accuracy:.2f}%")
    print(f"- Mean processing time: {avg_processing_ms:.2f} ms/image")
    print(f"- Mean throughput: {avg_throughput:.2f} images/min")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark the bundled visual inspection test images."
    )
    parser.add_argument(
        "image_dir",
        nargs="?",
        type=Path,
        default=Path("tests/imgs/test"),
        help="Directory containing images to evaluate.",
    )
    args = parser.parse_args()
    print_markdown(evaluate_images(args.image_dir))


if __name__ == "__main__":
    main()