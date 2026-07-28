import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.analytics import create_charts, load_summaries, write_comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Menggabungkan laporan eksperimen")
    parser.add_argument("--reports", type=Path, default=Path("reports"))
    parser.add_argument("--output", type=Path, default=Path("reports/aggregate"))
    args = parser.parse_args()
    summaries = load_summaries(args.reports)
    summaries = [item for item in summaries if Path(item["report_dir"]) != args.output]
    if not summaries:
        parser.error("Belum ada summary.json yang dapat digabungkan")
    comparison = write_comparison(summaries, args.output)
    charts = create_charts(summaries, args.output)
    print(f"Perbandingan: {comparison}")
    for chart in charts:
        print(f"Grafik: {chart}")


if __name__ == "__main__":
    main()
