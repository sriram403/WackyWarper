import argparse
import random
import os
import cv2
from pathlib import Path

COLORS = [
    (56, 56, 255), (151, 157, 255), (31, 112, 255), (29, 178, 255),
    (49, 210, 207), (10, 249, 72),  (23, 204, 146), (134, 219, 61),
    (52, 147, 26),  (187, 212, 0),  (168, 153, 44), (255, 194, 0),
    (147, 69, 52),  (255, 115, 100),(236, 24, 0),   (255, 56, 56),
]

def draw_boxes(image_path, label_path, class_names):
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    h, w = img.shape[:2]

    if label_path.exists():
        lines = label_path.read_text().strip().splitlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            cls = int(parts[0])
            x_c, y_c, bw, bh = map(float, parts[1:5])

            x1 = int((x_c - bw / 2) * w)
            y1 = int((y_c - bh / 2) * h)
            x2 = int((x_c + bw / 2) * w)
            y2 = int((y_c + bh / 2) * h)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            color = COLORS[cls % len(COLORS)]
            label = class_names[cls] if cls < len(class_names) else str(cls)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
            cv2.putText(img, label, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return img


def collect_pairs(folder):
    """Return list of (image_path, label_path) from a folder.
    Handles both flat layout (images/ labels/) and split layout (Train/images/ etc.)."""
    folder = Path(folder)
    pairs = []

    # Try split layout: Train/images, Valid/images, Test/images
    for split in ["Train", "Valid", "Test"]:
        img_dir = folder / split / "images"
        lbl_dir = folder / split / "labels"
        if img_dir.exists():
            for img in img_dir.iterdir():
                if img.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                    lbl = lbl_dir / (img.stem + ".txt")
                    pairs.append((img, lbl))

    # Flat layout: images/ labels/
    if not pairs:
        img_dir = folder / "images"
        lbl_dir = folder / "labels"
        if img_dir.exists():
            for img in img_dir.iterdir():
                if img.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                    lbl = lbl_dir / (img.stem + ".txt")
                    pairs.append((img, lbl))

    return pairs


parser = argparse.ArgumentParser(description="Visualize YOLO annotations on augmented images")
parser.add_argument("folder",           help="Augmented dataset folder (e.g. V16_dlt_Data)")
parser.add_argument("-n", "--count",    type=int, default=20,   help="Number of random images (default: 20)")
parser.add_argument("-o", "--output",   default="visualized",   help="Output folder (default: visualized/)")
parser.add_argument("-c", "--classes",  nargs="*", default=[],  help="Class names in order, e.g. -c adult child")
args = parser.parse_args()

pairs = collect_pairs(args.folder)
if not pairs:
    print(f"No images found in {args.folder}")
    exit(1)

sample = random.sample(pairs, min(args.count, len(pairs)))
out_dir = Path(args.output)
out_dir.mkdir(exist_ok=True)

saved = 0
for img_path, lbl_path in sample:
    result = draw_boxes(img_path, lbl_path, args.classes)
    if result is None:
        continue
    out_path = out_dir / f"viz_{img_path.stem}.jpg"
    cv2.imwrite(str(out_path), result)
    saved += 1

print(f"Saved {saved} annotated images to {out_dir}/")
