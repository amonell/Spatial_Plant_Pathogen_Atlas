"""Calculates and stores various statistics and quality metrics.

This module should generally not be interacted with directly, but rather through an instance of
the MerfishExperiment class (see experiment.py).
"""

import os
import json
import random
from functools import cached_property

import h5py
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.linalg import norm
from scipy.stats import pearsonr

import src.config as config
import src.plotting as plotting
import src.fileio as fileio

stats = {}
savefile = None


def set(key: str, value: float, silent: bool = False) -> None:
    stats[key] = value
    if not silent:
        print(f"{key}: {value}")
    if savefile:
        fileio.save_stats(stats, savefile)


def get(key: str) -> float:
    return stats[key]
