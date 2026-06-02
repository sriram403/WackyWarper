import argparse
import re
import shutil
from pathlib import Path

from tqdm import tqdm

# Expected filename: {cam_id}_{YYYY}_{MM}_{DD}T{HH}_{MM}_{SS}.{ms}Z_{frame}.{ext}
FILE_PATTERN = re.compile(
    r"^([A-Za-z0-9]+)_(\d{4})_(\d{2})_(\d{2})T(\d{2})_(\d{2})_(\d{2})\.\d+Z_\d+\.(jpg|txt)$"
)


def build_output_name(stem_match, cam_view: str, version: str, ext: str) -> str:
    cam_id, yyyy, mm, dd, hh, mi, ss = stem_match.groups()[:7]
    yy = yyyy[2:]
    return f"{cam_id}_{yy}{mm}{dd}_{hh}_{mi}_{ss}_{cam_view}_{version}.{ext}"


def main():
    parser = argparse.ArgumentParser(description="Separate images and labels into flat output folders.")
    parser.add_argument("--cam_view", required=True, help='Camera view tag, e.g. "Indoor"')
    parser.add_argument("--version", required=True, help='Version tag, e.g. "V16"')
    parser.add_argument("--input_dir", default="Unzipped", help="Root of the unzipped folder (default: Unzipped)")
    parser.add_argument("--output_dir", default="output", help="Destination root; images/ and labels/ created inside (default: output)")
    args = parser.parse_args()

    input_root = Path(args.input_dir)
    if not input_root.exists():
        raise SystemExit(f"Input directory not found: {input_root}")

    images_dir = Path(args.output_dir) / "images"
    labels_dir = Path(args.output_dir) / "labels"
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)

    all_files = [
        f for f in input_root.rglob("*")
        if f.is_file() and FILE_PATTERN.match(f.name)
    ]

    if not all_files:
        raise SystemExit("No matching files found. Check --input_dir path.")

    skipped = 0
    for src in tqdm(all_files, desc="Processing files", unit="file"):
        m = FILE_PATTERN.match(src.name)
        ext = src.suffix.lstrip(".")
        dest_name = build_output_name(m, args.cam_view, args.version, ext)

        dest_dir = images_dir if ext == "jpg" else labels_dir
        dest = dest_dir / dest_name

        if dest.exists():
            skipped += 1
            continue

        shutil.copy2(src, dest)

    print(f"\nDone. {len(all_files) - skipped} files copied, {skipped} skipped (already existed).")
    print(f"  Images -> {images_dir}")
    print(f"  Labels -> {labels_dir}")


if __name__ == "__main__":
    main()
