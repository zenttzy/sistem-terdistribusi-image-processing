from pathlib import Path
from time import perf_counter

import cv2


def process_image(input_path: Path, output_path: Path) -> dict:
    started_at = perf_counter()
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError(f"Gambar tidak dapat dibaca: {input_path}")

    height, width = image.shape[:2]
    target_width = min(width, 1920)
    target_height = max(1, round(height * target_width / width))
    resized = cv2.resize(image, (target_width, target_height))
    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (11, 11), 0)
    edges = cv2.Canny(blurred, 50, 150)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), edges):
        raise OSError(f"Gagal menyimpan hasil: {output_path}")

    return {
        "input_file": str(input_path),
        "output_file": str(output_path),
        "width": width,
        "height": height,
        "duration_seconds": perf_counter() - started_at,
        "status": "SUCCESS",
    }

