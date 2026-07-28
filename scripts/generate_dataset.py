import argparse
from pathlib import Path

import cv2
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser(description="Membuat dataset gambar sintetis")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--output", type=Path, default=Path("dataset"))
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    random = np.random.default_rng(seed=42)
    for index in range(1, args.count + 1):
        image = random.integers(0, 256, (args.height, args.width, 3), dtype=np.uint8)
        cv2.putText(image, f"Sample {index:04d}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
        cv2.imwrite(str(args.output / f"sample_{index:04d}.jpg"), image)
    print(f"Berhasil membuat {args.count} gambar di {args.output}")


if __name__ == "__main__":
    main()

