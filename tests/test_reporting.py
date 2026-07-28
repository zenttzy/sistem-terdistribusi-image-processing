from app.reporting import build_summary


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

