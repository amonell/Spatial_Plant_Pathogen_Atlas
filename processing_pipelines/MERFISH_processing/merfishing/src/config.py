"""Global configuration settings for the pipeline."""

import json
import os

config = {
    "omit_fovs": [],
    "reference_counts": [],
    "mask_size": 2048,
    "transpose_barcodes": False,
    "flip_barcodes": False,
    "scale": 1,
}
result_path = None


def get(key: str):
    return config[key]


def has(key: str) -> bool:
    return key in config


def update(settings: dict) -> None:
    for key, value in settings.items():
        config[key] = value


def load_from_file(config_file: str) -> None:
    global config
    with open(config_file) as conf:
        config.update(json.loads(conf.read()))


def load(args):
    global config
    if args.config_file:
        load_from_file(args.config_file)
    for key, value in vars(args).items():
        if value is None:
            continue
        config[key] = value
    config["scale"] = 2048 / config["mask_size"]


def path(filename):
    global result_path
    if result_path is None:
        result_path = os.path.join(
            get("analysis_root"), get("experiment_name"), get("result_folder")
        )
        if not os.path.exists(result_path):
            os.mkdir(result_path)
    return os.path.join(result_path, filename)
