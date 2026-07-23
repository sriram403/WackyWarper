# WackyWarper

A YOLO dataset augmentation and splitting pipeline built on [Albumentations](https://albumentations.ai/).

---

## Features

- **Dataset splitting** — random custom split or scikit-learn stratified split into Train / Valid / Test
- **Image augmentation** — bounding-box-aware augmentations using Albumentations (flip, rotate, blur, color jitter, etc.)
- **Flexible pipeline** — run splitting only, augmentation only, or both
- **Progress bars** — tqdm progress for both splitting and augmentation steps
- **Utility scripts** — organize raw zip files and visualize annotated outputs

---

## Installation

```bash
pip install opencv-python albumentations scikit-learn tqdm
```

---

## Quick Start

```python
from WackyWarper import Whole_PipeLine

Whole_PipeLine.Give_Me_Augmented_Data(
    IMG_DIR="images/",
    LABEL_DIR="labels/",
    VALID_RATIO=0.20,
    TEST_RATIO=0.05,
    SKLEARN_SPLIT=True,
    AUGMENTED_HEADER_NAME="Data",
    NUMBER_OF_IMAGES_NEEDED=3,
)
```

Output structure:
```
Data/
  Train/
    images/
    labels/
  Valid/
    images/
    labels/
  Test/
    images/
    labels/
```

---

## Pipeline Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `IMG_DIR` | str | — | Path to source images folder |
| `LABEL_DIR` | str | — | Path to source YOLO labels folder |
| `VALID_RATIO` | float | — | Fraction of data for validation |
| `TEST_RATIO` | float | `0.05` | Fraction of validation split used for test |
| `SKLEARN_SPLIT` | bool | — | `True` = sklearn split, `False` = custom random split |
| `TRAIN_RATIO` | float | `0.8` | Used only when `SKLEARN_SPLIT=False` |
| `AUGMENTED_HEADER_NAME` | str | — | Output folder name |
| `NUMBER_OF_IMAGES_NEEDED` | int | — | Augmented copies per image |
| `SPLIT` | bool | `True` | Set `False` to skip splitting (use existing `Splitted/`) |
| `AUGMENT` | bool | `True` | Set `False` to skip augmentation (split only) |
| `OLD_IMG_DIR` | str | `None` | Optional older/previous image folder, merged with `IMG_DIR` before splitting |
| `OLD_LABEL_DIR` | str | `None` | Optional older/previous label folder, merged with `LABEL_DIR` before splitting |

> In [main.py](main.py), the `OLD_IMG_DIR`/`OLD_LABEL_DIR` values are controlled by a single `old_and_new_mix` flag (default `True`). Set `old_and_new_mix = False` to ignore the old dataset and split/augment only the new `output/images` + `output/labels` data.

### Split only

```python
Whole_PipeLine.Give_Me_Augmented_Data(
    ...,
    SPLIT=True,
    AUGMENT=False,
)
```

### Augment only (reuse existing split)

```python
Whole_PipeLine.Give_Me_Augmented_Data(
    ...,
    SPLIT=False,
    AUGMENT=True,
)
```

---

## Augmentation Config

Augmentation transforms are defined in [WackyWarper/config/albumentation_custom.py](WackyWarper/config/albumentation_custom.py). Every image is run through the pipeline once per `NUMBER_OF_IMAGES_NEEDED`, and each transform below is applied independently with its own probability `p` (so several can fire on the same image at once).

There are **two** Albumentations pipelines defined side by side:

- `augmentor` — used when the source label has bounding boxes (`bbox_params` keeps boxes in sync with the image transform)
- `augmentor_without_boudingbox` — used when there are no boxes for that image (no `bbox_params`, so it also runs `RandomGamma`, which isn't box-aware)

`Augmentor.py` picks whichever one applies per image automatically — you don't select this yourself.

| Transform | Variable(s) | Current value | Effect | Active in |
|---|---|---|---|---|
| `HorizontalFlip` | `HF` | `0.5` | Probability of flipping the image left-right | both |
| `RandomBrightnessContrast` | `RBC` | `0.2` | Probability of randomly shifting brightness/contrast | both |
| `Rotate` | `LIMIT`, `VALUE_TO_ROTATE` | `10°` max, `p=0.2` | Rotates image ± up to `LIMIT` degrees, with probability `VALUE_TO_ROTATE` | both |
| `Blur` | `B` | `0.2` | Probability of applying a blur kernel | both |
| `ColorJitter` | `CJ_BRIGHTNESS`, `CJ_CONTRAST`, `CJ_SATURATION`, `CJ_VALUE` | `0.2` each | Randomly jitters brightness/contrast/saturation, with probability `CJ_VALUE` | both |
| `RandomGamma` | `RG` | `0.2` | Probability of applying gamma correction | **no-bbox pipeline only** |
| `RGBShift` | `RGBS` | `0.2` | Probability of randomly shifting R/G/B channel intensities | both |
| `VerticalFlip` | `VF` | `0.8` | Probability of flipping the image top-bottom | both |
| `RandomCrop` | `W`, `H` | `1000×1000` | Crops to a fixed size before other transforms | **disabled** (commented out in both pipelines) |

### Where and how to change it

All of it lives in the same file: `WackyWarper/config/albumentation_custom.py`.

- **Tune an existing transform** — edit its constant at the top of the file (e.g. change `VF = 0.8` to `VF = 0.5` to flip vertically half as often, or `LIMIT = 10` to `LIMIT = 20` for wider rotation angles). No other file needs to change.
- **Turn a transform off** — comment out (or delete) its line inside the `alb.Compose([...])` list(s). Do this in both `augmentor` and `augmentor_without_boudingbox` if you want it off everywhere.
- **Turn `RandomCrop` on** — uncomment the `alb.RandomCrop(width=W, height=H)` line in both `Compose([...])` lists and adjust `W`/`H` if needed.
- **Add a new Albumentations transform** — import/use it same as the others (`alb.<Transform>(...)`) and add it to the `Compose([...])` list(s); add it to both pipelines if it should apply regardless of whether boxes exist, or only one if it's box-aware / box-incompatible like `RandomGamma`.
- After any change, no rebuild is needed — `main.py` (via `Whole_PipeLine` → `Augmentor`) re-imports this module fresh on every run.

---

## Utility Scripts

### move_zips.py

Moves all `.zip` files from `data/` into `data/Indoor/` or `data/Outdoor/`.

```bash
python move_zips.py indoor
python move_zips.py outdoor
```

### visualize.py

Draws YOLO bounding boxes on random images from an augmented dataset and saves annotated JPGs.

```bash
# Basic usage
python visualize.py V16_dlt_Data

# With class names, custom count, custom output folder
python visualize.py V16_dlt_Data -n 30 -c adult child -o visualized/
```

| Argument | Default | Description |
|---|---|---|
| `folder` | — | Augmented dataset folder |
| `-n` / `--count` | `20` | Number of random images to visualize |
| `-c` / `--classes` | class IDs | Class names in label order |
| `-o` / `--output` | `visualized/` | Output folder for annotated images |

Supports both flat (`images/`, `labels/`) and split (`Train/images/`, etc.) folder layouts.

---

## Label Format

YOLO format — one `.txt` per image, one detection per line:

```
<class_id> <x_center> <y_center> <width> <height>
```

All values normalized to `[0, 1]`.

---

## Links

- [LinkedIn](https://www.linkedin.com/in/sriram36/)
- [Twitter](https://twitter.com/sriram93298?t=Slkk-hhkX8nmGKV4PPAIzg&s=09)
