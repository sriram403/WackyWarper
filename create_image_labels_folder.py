import argparse
import re
import shutil
from pathlib import Path

from tqdm import tqdm

# Expected filename: {cam_id}_{YYYY}_{MM}_{DD}T{HH}_{MM}_{SS}.{ms}Z_{frame}.{ext}
FILE_PATTERN = re.compile(
    r"^([A-Za-z0-9]+)_(\d{4})_(\d{2})_(\d{2})T(\d{2})_(\d{2})_(\d{2})\.\d+Z_\d+\.(jpg|txt)$"
)

VIEW_TAGS = ("Indoor", "Outdoor")


def detect_cam_view(path: Path):
    """Find the Indoor/Outdoor tag from the file's parent folders."""
    parts_lower = {p.lower() for p in path.parts}
    for tag in VIEW_TAGS:
        if tag.lower() in parts_lower:
            return tag
    return None


def build_output_name(stem_match, cam_view: str, version: str, ext: str) -> str:
    cam_id, yyyy, mm, dd, hh, mi, ss = stem_match.groups()[:7]
    yy = yyyy[2:]
    return f"{cam_id}_{yy}{mm}{dd}_{hh}_{mi}_{ss}_{cam_view}_{version}.{ext}"


def main():
    parser = argparse.ArgumentParser(
        description="Separate images and labels into flat output folders, "
        "auto-tagging each file as Indoor/Outdoor from its folder path."
    )
    parser.add_argument("--version", required=True, help='Version tag, e.g. "V17"')
    parser.add_argument(
        "--input_dir",
        default=str(Path(__file__).parent.parent / "extracted"),
        help="Root of the unzipped folder (default: extracted/ above the script's folder)",
    )
    parser.add_argument("--output_dir", default="output", help="Destination root; images/ and labels/ created inside (default: output)")
    args = parser.parse_args()

    input_root = Path(args.input_dir)
    if not input_root.exists():
        raise SystemExit(f"Input directory not found: {input_root}")

    images_dir = Path(args.output_dir) / "images"
    labels_dir = Path(args.output_dir) / "labels"
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)

    all_files = [f for f in input_root.rglob("*") if f.is_file() and FILE_PATTERN.match(f.name)]

    if not all_files:
        raise SystemExit("No matching files found. Check --input_dir path.")

    skipped = 0
    unresolved = []
    for src in tqdm(all_files, desc="Processing files", unit="file"):
        cam_view = detect_cam_view(src)
        if cam_view is None:
            unresolved.append(src)
            continue

        m = FILE_PATTERN.match(src.name)
        ext = src.suffix.lstrip(".")
        dest_name = build_output_name(m, cam_view, args.version, ext)

        dest_dir = images_dir if ext == "jpg" else labels_dir
        dest = dest_dir / dest_name

        if dest.exists():
            skipped += 1
            continue

        shutil.copy2(src, dest)

    copied = len(all_files) - skipped - len(unresolved)
    num_images = sum(1 for _ in images_dir.iterdir())
    num_labels = sum(1 for _ in labels_dir.iterdir())
    print(f"\nDone. {copied} files copied, {skipped} skipped (already existed), {len(unresolved)} skipped (no Indoor/Outdoor tag in path).")
    print(f"  Images -> {images_dir} ({num_images} files)")
    print(f"  Labels -> {labels_dir} ({num_labels} files)")

    if unresolved:
        print("\nFiles with no Indoor/Outdoor tag found in their path (first 10):")
        for f in unresolved[:10]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
