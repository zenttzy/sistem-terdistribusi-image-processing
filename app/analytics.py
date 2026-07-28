import csv
import json
from pathlib import Path


def load_summaries(reports_dir: Path) -> list[dict]:
    summaries = []
    for path in sorted(reports_dir.glob("*/summary.json")):
        summary = json.loads(path.read_text(encoding="utf-8"))
        summary["report_dir"] = str(path.parent)
        summaries.append(summary)
    return summaries


def write_comparison(summaries: list[dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison_path = output_dir / "comparison.csv"
    fields = ["mode", "workers", "total_images", "successful", "failed", "wall_time_seconds", "throughput_images_per_second", "speedup", "efficiency_percent"]
    rows = []
    for item in summaries:
        baseline_item = next(
            (
                candidate
                for candidate in summaries
                if candidate["mode"] == "sequential"
                and candidate.get("total_images") == item.get("total_images")
            ),
            None,
        )
        baseline = baseline_item["wall_time_seconds"] if baseline_item else None
        speedup = baseline / item["wall_time_seconds"] if baseline and item["wall_time_seconds"] else 0
        workers = item.get("workers", 1)
        rows.append({**item, "speedup": speedup, "efficiency_percent": speedup / workers * 100 if workers else 0})
    with comparison_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return comparison_path


def create_charts(summaries: list[dict], output_dir: Path) -> list[Path]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output_dir.mkdir(parents=True, exist_ok=True)
    labels = [f"{item['mode']} ({item.get('workers', 1)}W)" for item in summaries]
    times = [item["wall_time_seconds"] for item in summaries]
    throughputs = [item["throughput_images_per_second"] for item in summaries]
    paths = []
    for name, values, ylabel in (("execution-time.png", times, "Seconds"), ("throughput.png", throughputs, "Images / second")):
        figure, axis = plt.subplots(figsize=(8, 4.5))
        axis.bar(labels, values)
        axis.set_ylabel(ylabel)
        axis.set_title(name.removesuffix(".png").replace("-", " ").title())
        axis.tick_params(axis="x", rotation=20)
        figure.tight_layout()
        path = output_dir / name
        figure.savefig(path, dpi=160)
        plt.close(figure)
        paths.append(path)
    return paths
