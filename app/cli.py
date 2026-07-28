import argparse
from datetime import datetime
from pathlib import Path
from time import perf_counter

from celery import group

from app.config import DATASET_DIR, OUTPUT_DIR, REPORTS_DIR, SUPPORTED_EXTENSIONS
from app.image_processor import process_image
from app.reporting import build_summary, write_report
from app.tasks import process_image_task


def discover_images(dataset_dir: Path) -> list[Path]:
    return sorted(
        path for path in dataset_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def failed_result(path: Path, error: Exception) -> dict:
    return {"input_file": str(path), "status": "FAILED", "error": str(error)}


def run_sequential(images: list[Path], output_dir: Path) -> list[dict]:
    results = []
    for image in images:
        try:
            results.append(process_image(image, output_dir / f"{image.stem}_edges.png"))
        except Exception as error:
            results.append(failed_result(image, error))
    return results


def run_distributed(images: list[Path], output_dir: Path, timeout: int) -> list[dict]:
    jobs = group(
        process_image_task.s(str(image), str(output_dir / f"{image.stem}_edges.png"))
        for image in images
    )()
    raw_results = jobs.get(timeout=timeout, propagate=False)
    results = []
    for image, result in zip(images, raw_results):
        if isinstance(result, Exception):
            results.append(failed_result(image, result))
        else:
            results.append(result)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Pemrosesan citra paralel dan terdistribusi")
    parser.add_argument("--mode", choices=("sequential", "distributed"), required=True)
    parser.add_argument("--dataset", type=Path, default=DATASET_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--reports", type=Path, default=REPORTS_DIR)
    parser.add_argument("--workers", type=int, default=1, help="Metadata jumlah worker eksperimen")
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    images = discover_images(args.dataset)
    if not images:
        parser.error(f"Tidak ada gambar ditemukan di {args.dataset}")

    experiment_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = args.output / experiment_id
    started_at = perf_counter()
    if args.mode == "sequential":
        results = run_sequential(images, output_dir)
    else:
        results = run_distributed(images, output_dir, args.timeout)
    wall_time = perf_counter() - started_at

    summary = build_summary(args.mode, results, wall_time, args.workers)
    report_dir = args.reports / experiment_id
    write_report(report_dir, results, summary)
    print(f"Eksperimen selesai: {report_dir / 'summary.json'}")
    print(f"Berhasil: {summary['successful']}/{summary['total_images']}")
    print(f"Waktu: {summary['wall_time_seconds']:.3f} detik")
    print(f"Throughput: {summary['throughput_images_per_second']:.3f} gambar/detik")


if __name__ == "__main__":
    main()
