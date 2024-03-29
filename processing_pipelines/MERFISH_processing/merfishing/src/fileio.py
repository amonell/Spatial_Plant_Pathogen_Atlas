import os
import re
import glob
import json
import pickle
from typing import Dict

import numpy as np
import pandas as pd
from tqdm import tqdm


def merlin_barcode_folder(merlin_dir: str) -> str:
    """Get the path to the folder containing the filtered barcode files."""
    return os.path.join(merlin_dir, "AdaptiveFilterBarcodes", "barcodes")


def merlin_raw_barcode_folder(merlin_dir: str) -> str:
    return os.path.join(merlin_dir, "Decode", "barcodes")


def merlin_raw_barcode_files(merlin_dir: str) -> list:
    return glob.glob(
        os.path.join(merlin_raw_barcode_folder(merlin_dir), "barcode_data_*.h5")
    )


def load_merlin_barcodes(barcode_file: str) -> pd.DataFrame:
    """Return the barcodes for the given FOV as a pandas DataFrame."""
    return pd.read_hdf(barcode_file)


def merlin_barcode_files(merlin_dir: str) -> list:
    return glob.glob(
        os.path.join(merlin_barcode_folder(merlin_dir), "barcode_data_*.h5")
    )


def load_vizgen_barcodes(output_folder: str) -> pd.DataFrame:
    bcs = []
    for bcfile in glob.glob(output_folder + "/region_*/detected_transcripts.csv"):
        print(bcfile)
        bcs.append(pd.read_csv(bcfile, index_col=0))
        bcfile = bcfile.replace("\\", "/")
        region = bcfile.split("/")[-2].split("_")[1]
        bcs[-1]["region"] = region
    return bcs.reset_index().drop(columns="index")
    #return pd.concat(bcs)bcs.reset_index().drop(columns="index")


def load_hyb_drifts(merlin_dir: str, fov: int) -> pd.DataFrame:
    """Get the drifts calculated between hybridization rounds for the given FOV.

    The 'X drift' and 'Y drift' columns indicate the translation required to
    align coordinates in the FOV and hybridization round to the first hybridization
    round for that FOV. These drifts are calculated by MERlin.
    """
    rows = []
    filename = os.path.join(
        merlin_dir, "FiducialBeadWarp", "transformations", f"offsets_{fov}.npy"
    )
    drifts = np.load(filename, allow_pickle=True)
    for bit, drift in enumerate(drifts, start=1):
        rows.append([fov, bit, drift.params[0][2], drift.params[1][2]])
    return pd.DataFrame(rows, columns=["FOV", "Bit", "X drift", "Y drift"])


def load_codebook(merlin_dir: str) -> pd.DataFrame:
    """Get the codebook used for this MERFISH experiment.

    The 'name' and 'id' columns are identical, and both contain the name of the
    gene or blank barcode encoded by that row. The 'bit1' through 'bitN' columns
    contain the 0s or 1s of the barcode.
    """
    return pd.read_csv(glob.glob(os.path.join(merlin_dir, "codebook_*.csv"))[0])


def load_fov_positions(merlin_dir: str) -> pd.DataFrame:
    """Get the global positions of the FOVs.

    The coordinates indicate the top-left corner of the FOV.
    """
    df = pd.read_csv(os.path.join(merlin_dir, "positions.csv"), header=None)
    df.columns = ["x", "y"]
    return df


def load_mask(segmask_dir: str, fov: int, pad: int = 6) -> np.ndarray:
    # Detect type of mask
    # if glob.glob(os.path.join(segmask_dir, "Conv_zscan*.png")):
    #    filename = os.path.join(segmask_dir, f"Conv_zscan_H0_F_{fov:03d}_cp_masks.png")
    #    return np.asarray(Image.open(filename))

    filename = os.path.join(segmask_dir, f"Fov-{fov:04d}_seg.pkl")
    if os.path.exists(filename):
        pkl = pickle.load(open(filename, "rb"))
        return pkl[0].astype(np.uint32)

    filename = os.path.join(segmask_dir, f"Conv_zscan_H0_F_{fov:0{pad}d}_seg.npy")
    if os.path.exists(filename):
        return np.load(filename, allow_pickle=True).item()["masks"]

    filename = os.path.join(segmask_dir, f"stack_prestain_{fov:0{pad}d}_seg.npy")
    if os.path.exists(filename):
        return np.load(filename, allow_pickle=True).item()["masks"]

    filename = os.path.join(segmask_dir, f"stack_prestain_"+str(fov).zfill(6)+"_cp_masks_cp_masks.png")
    if os.path.exists(filename):
        from PIL import Image

        return np.asarray(Image.open(filename))

    raise Exception(f"No mask found in {segmask_dir} for FOV {fov}")


def load_all_masks(segmask_dir: str, n_fovs: int, pad: int = None) -> list:
    if pad is None:
        pad = len(str(n_fovs))
    return [
        load_mask(segmask_dir, fov, pad)
        for fov in tqdm(range(n_fovs), desc="Loading cell masks")
    ]


def save_cell_links(links, filename):
    with open(filename, "w") as f:
        for link in links:
            print(repr(link), file=f)


def load_cell_links(filename):
    links = []
    with open(filename) as f:
        for line in f:
            links.append(eval(line))
    return links


def save_barcode_table(barcodes, filename):
    barcodes.to_csv(filename, index=False)


def load_barcode_table(filename):
    return pd.read_csv(filename)


def save_cell_metadata(celldata, filename):
    celldata.to_csv(filename)


def load_cell_metadata(filename):
    return pd.read_csv(filename, index_col=0)


def save_cell_by_gene_table(cellbygene, filename):
    cellbygene.to_csv(filename)


def load_cell_by_gene_table(filename):
    return pd.read_csv(filename, index_col=0)


def save_stats(stats, filename) -> None:
    text = json.dumps(stats, indent=4)
    with open(filename, "w") as f:
        f.write(text)


def load_stats(filename):
    return json.load(open(filename))


class DaxFile:
    def __init__(self, filename, num_channels=None):
        self.filename = filename
        self.num_channels = num_channels
        self._info = None
        self._memmap = np.memmap(
            filename,
            dtype=np.uint16,
            mode="r",
            shape=(
                self.fileinfo("frames"),
                self.fileinfo("height"),
                self.fileinfo("width"),
            ),
        )
        if self.fileinfo("endian") == 1:
            self._memmap = self._memmap.byteswap()

    def __getitem__(self, key):
        return self._memmap[key]

    def logmsg(self, message):
        return f"Dax file {self.filename} - {message}"

    def fileinfo(self, tag):
        if self._info is None:
            self.load_fileinfo()
        return self._info[tag]

    def load_fileinfo(self):
        with open(self.filename.replace(".dax", ".inf")) as f:
            infodata = f.read()
        self._info = {}
        m = re.search(r"frame dimensions = ([\d]+) x ([\d]+)", infodata)
        self._info["height"] = int(m.group(1))
        self._info["width"] = int(m.group(2))
        m = re.search(r"number of frames = ([\d]+)", infodata)
        self._info["frames"] = int(m.group(1))
        m = re.search(r" (big|little) endian", infodata)
        self._info["endian"] = 1 if m.group(1) == "big" else 0

    def channel(self, channel):
        return self._memmap[channel :: self.num_channels, :, :]

    def get_entire_image(self):
        return self._memmap[:, :, :]

    def zslice(self, zslice, channel=None):
        """If channel is None, return all channels."""
        if channel is None:
            return self._memmap[
                zslice * self.num_channels : zslice * self.num_channels
                + self.num_channels,
                :,
                :,
            ]
        else:
            return self._memmap[channel + zslice * self.num_channels, :, :]

    def frame(self, frame):
        return self._memmap[frame, :, :]

    def max_projection(self, channel=None):
        if channel is None:
            return np.max(self._memmap[:, :, :], axis=0)
        else:
            return np.max(self._memmap[channel :: self.num_channels, :, :], axis=0)

    def block_range(self, xr=None, yr=None, zr=None, channel=None):
        if xr is None:
            xr = (0, self.fileinfo("width"))
        if yr is None:
            yr = (0, self.fileinfo("height"))
        if zr is None:
            zr = (0, self.fileinfo("frames"))
        if xr[0] < 0:
            xr = (0, xr[1])
        if yr[0] < 0:
            yr = (0, yr[1])
        if zr[0] < 0:
            zr = (0, zr[1])
        if channel is None:
            zslice = slice(self.num_channels * zr[0], self.num_channels * (zr[1] + 1))
        else:
            zslice = slice(
                self.num_channels * zr[0] + channel,
                self.num_channels * (zr[1] + 1) + channel,
                self.num_channels,
            )
        yslice = slice(yr[0], yr[1] + 1)
        xslice = slice(xr[0], xr[1] + 1)
        return self._memmap[zslice, yslice, xslice], (zslice, yslice, xslice)

    def block(self, center, volume, channel=None):
        zr = (center[0] - volume[0], center[0] + volume[0])
        yr = (center[1] - volume[1], center[1] + volume[1])
        xr = (center[2] - volume[2], center[2] + volume[2])
        return self.block_range(zr=zr, yr=yr, xr=xr, channel=channel)
