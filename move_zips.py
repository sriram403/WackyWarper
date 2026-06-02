import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description="Move zip files into Indoor or Outdoor folder inside data/")
parser.add_argument("location", choices=["Indoor", "Outdoor"], help="Target folder: indoor or outdoor")
args = parser.parse_args()

data_dir = Path(__file__).parent / "data"
target_dir = data_dir / args.location.capitalize()
target_dir.mkdir(exist_ok=True)

zip_files = list(data_dir.glob("*.zip"))

if not zip_files:
    print("No zip files found in data/")
else:
    for zip_file in zip_files:
        dest = target_dir / zip_file.name
        shutil.move(str(zip_file), str(dest))
        print(f"Moved {zip_file.name} -> {target_dir.name}/")

    print(f"\nDone. {len(zip_files)} zip file(s) moved to data/{target_dir.name}/")
