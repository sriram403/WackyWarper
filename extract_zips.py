import zipfile
from pathlib import Path

from tqdm import tqdm

source_dir = Path(__file__).parent.parent
target_dir = source_dir / "extracted"
target_dir.mkdir(exist_ok=True)

CHUNK_SIZE = 16 * 1024 * 1024

zip_files = list(source_dir.glob("*.zip"))

if not zip_files:
    print(f"No zip files found in {source_dir}/")
else:
    for zip_path in tqdm(zip_files, desc="Overall progress", unit="file"):
        with zipfile.ZipFile(zip_path) as zf:
            members = zf.infolist()
            total_size = sum(member.file_size for member in members)

            with tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024,
                desc=zip_path.name, leave=False,
            ) as pbar:
                for member in members:
                    dest_path = target_dir / member.filename

                    if member.is_dir():
                        dest_path.mkdir(parents=True, exist_ok=True)
                        continue

                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as fsrc, open(dest_path, "wb") as fdst:
                        while True:
                            chunk = fsrc.read(CHUNK_SIZE)
                            if not chunk:
                                break
                            fdst.write(chunk)
                            pbar.update(len(chunk))

        zip_path.unlink()
        tqdm.write(f"Extracted {zip_path.name} -> {target_dir}/ (and removed zip)")

    print(f"\nDone. {len(zip_files)} zip file(s) extracted to {target_dir}/")
