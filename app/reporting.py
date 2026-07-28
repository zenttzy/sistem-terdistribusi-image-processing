import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def build_summary(mode: str, results: list[dict], wall_time: float, workers: int) -> dict:
    successful = [result for result in results if result.get("status") == "SUCCESS"]
    failed = [result for result in results if result.get("status") != "SUCCESS"]
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "workers": workers,
        "total_images": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "wall_time_seconds": wall_time,
        "sum_task_time_seconds": sum(item.get("duration_seconds", 0) for item in successful),
        "throughput_images_per_second": len(successful) / wall_time if wall_time else 0,
    }


def write_report(report_dir: Path, results: list[dict], summary: dict) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    fieldnames = sorted({key for result in results for key in result})
    with (report_dir / "task-results.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

