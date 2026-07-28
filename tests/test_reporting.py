from app.reporting import build_summary
from app.analytics import write_comparison


def test_build_summary_calculates_metrics():
    results = [
        {"status": "SUCCESS", "duration_seconds": 0.5},
        {"status": "SUCCESS", "duration_seconds": 0.7},
        {"status": "FAILED", "error": "broken"},
    ]
    summary = build_summary("sequential", results, wall_time=2.0, workers=1)
    assert summary["total_images"] == 3
    assert summary["successful"] == 2
    assert summary["failed"] == 1
    assert summary["sum_task_time_seconds"] == 1.2
    assert summary["throughput_images_per_second"] == 1.0


def test_write_comparison_calculates_speedup(tmp_path):
    summaries = [
        {"mode": "sequential", "workers": 1, "total_images": 10, "successful": 10, "failed": 0, "wall_time_seconds": 10.0, "throughput_images_per_second": 1.0},
        {"mode": "distributed", "workers": 2, "total_images": 10, "successful": 10, "failed": 0, "wall_time_seconds": 5.0, "throughput_images_per_second": 2.0},
    ]
    path = write_comparison(summaries, tmp_path)
    rows = list(__import__("csv").DictReader(path.open()))
    assert float(rows[1]["speedup"]) == 2.0
    assert float(rows[1]["efficiency_percent"]) == 100.0


def test_write_comparison_matches_baseline_by_dataset_size(tmp_path):
    summaries = [
        {"mode": "sequential", "workers": 1, "total_images": 10, "successful": 10, "failed": 0, "wall_time_seconds": 1.0, "throughput_images_per_second": 10.0},
        {"mode": "sequential", "workers": 1, "total_images": 100, "successful": 100, "failed": 0, "wall_time_seconds": 10.0, "throughput_images_per_second": 10.0},
        {"mode": "distributed", "workers": 2, "total_images": 100, "successful": 100, "failed": 0, "wall_time_seconds": 5.0, "throughput_images_per_second": 20.0},
    ]
    path = write_comparison(summaries, tmp_path)
    rows = list(__import__("csv").DictReader(path.open()))
    assert float(rows[2]["speedup"]) == 2.0
