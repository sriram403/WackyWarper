import argparse
from pathlib import Path

from tqdm import tqdm

# Filenames (as they appear in data/) to copy (or move) to the local dir.
FILES_TO_MOVE = [
    "1st Month.zip",
    "2nd Month.zip",
    "3rd Month.zip",
    "4th Month.zip",
    "5th Month.zip",
    "6th Month.zip",
]

parser = argparse.ArgumentParser(description="Copy (default) or move zip files from data/ to the local dir.")
parser.add_argument("--move", action="store_true", help="Delete the source zip from data/ after copying (default: keep it, i.e. copy only)")
args = parser.parse_args()

data_dir = Path(__file__).parent.parent / "data"
target_dir = Path(__file__).parent.parent

CHUNK_SIZE = 16 * 1024 * 1024

zip_files = []
for name in FILES_TO_MOVE:
    zip_file = data_dir / name
    if zip_file.is_file():
        zip_files.append(zip_file)
    else:
        print(f"Skipping {name}: not found in {data_dir}/")

if not zip_files:
    print("No matching zip files found in data/")
else:
    for zip_file in tqdm(zip_files, desc="Overall progress", unit="file"):
        dest = target_dir / zip_file.name
        size = zip_file.stat().st_size

        with open(zip_file, "rb") as fsrc, open(dest, "wb") as fdst, tqdm(
            total=size, unit="B", unit_scale=True, unit_divisor=1024,
            desc=zip_file.name, leave=False,
        ) as pbar:
            while True:
                chunk = fsrc.read(CHUNK_SIZE)
                if not chunk:
                    break
                fdst.write(chunk)
                pbar.update(len(chunk))

        if args.move:
            zip_file.unlink()
            tqdm.write(f"Moved {zip_file.name} -> {target_dir}/")
        else:
            tqdm.write(f"Copied {zip_file.name} -> {target_dir}/")

    action = "moved" if args.move else "copied"
    print(f"\nDone. {len(zip_files)} zip file(s) {action} to {target_dir}/")
