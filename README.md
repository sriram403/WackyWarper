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

Augmentation transforms are defined in `WackyWarper/config/albumentation_custom.py`. Edit the probability and magnitude values there to customize the pipeline.

```python
HF = 0.5     # HorizontalFlip probability
RBC = 0.2    # RandomBrightnessContrast probability
LIMIT = 10   # Max rotation angle
B = 0.2      # Blur probability
VF = 0.8     # VerticalFlip probability
# ...
```

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
