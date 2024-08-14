from pathlib import Path


def get_data_dir():
    base_dir = Path.cwd().joinpath(".quatex")
    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_hist_dir():
    hist_dir = get_data_dir().joinpath("hist")
    if not hist_dir.exists():
        hist_dir.mkdir(parents=True, exist_ok=True)
    return hist_dir
