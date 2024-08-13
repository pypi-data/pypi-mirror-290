import pickle as pkl
from pathlib import Path


def save_to_pkl(obj: dict, path) -> Path:
    path = Path(path).with_suffix(".pkl")
    with open(path, "wb") as f:
        pkl.dump(obj, f)
    return path


def load_from_pkl(path):
    path = Path(path).with_suffix(".pkl")
    with open(path, "rb") as f:
        return pkl.load(f)
