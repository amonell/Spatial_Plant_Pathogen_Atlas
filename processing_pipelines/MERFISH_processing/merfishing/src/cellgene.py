import os
from random import sample
from functools import cached_property

import scanpy as sc
import numpy as np
from anndata import AnnData
from tqdm import tqdm

import src.stats as stats


def create_scanpy_object(cellgene, celldata, positions):
    blank_cols = np.array(
        ["notarget" in col or "blank" in col.lower() for col in cellgene]
    )
    adata = sc.AnnData(cellgene.loc[:, ~blank_cols], dtype=np.int32)
    adata.obsm["X_blanks"] = cellgene.loc[:, blank_cols].to_numpy()
    adata.uns["blank_names"] = cellgene.columns[blank_cols].to_list()
    adata.obsm["X_spatial"] = np.array(
        celldata[["global_x", "global_y"]].reindex(index=adata.obs.index.astype(int))
    )
    adata.obsm["X_local"] = np.array(
        celldata[["fov_x", "fov_y"]].reindex(index=adata.obs.index.astype(int))
    )
    celldata.index = celldata.index.astype(str)
    adata.obs["volume"] = celldata["volume"]
    adata.obs["fov"] = celldata["fov"].astype(str)
    adata.layers["counts"] = adata.X
    adata.uns["fov_positions"] = positions.to_numpy()
    sc.pp.calculate_qc_metrics(adata, percent_top=None, inplace=True)
    adata.obs["blank_counts"] = adata.obsm["X_blanks"].sum(axis=1)
    adata.obs["misid_rate"] = (
        adata.obs["blank_counts"] / len(adata.uns["blank_names"])
    ) / (adata.obs["total_counts"] / len(adata.var_names))
    adata.obs["counts_per_volume"] = adata.obs["total_counts"] / adata.obs["volume"]
    return adata


def adjust_spatial_coordinates(
    adata, flip_horizontal=False, flip_vertical=False, transpose=False
):
    if transpose and (flip_horizontal or flip_vertical):
        pass  # TODO: Should warn about order of operations
    if transpose:
        adata.obsm["X_spatial"] = np.roll(adata.obsm["X_spatial"], 1, 1)
    if flip_horizontal:
        adata.obsm["X_spatial"][:, 0] = -adata.obsm["X_spatial"][:, 0]
    if flip_vertical:
        adata.obsm["X_spatial"][:, 1] = -adata.obsm["X_spatial"][:, 1]


def normalize(adata, scale=False):
    sc.pp.normalize_total(adata)
    sc.pp.log1p(adata, base=2)
    adata.raw = adata
    if scale:
        sc.pp.scale(adata)
    return adata


def optimize_number_PCs(adata):
    def jumble(seq):
        return sample(list(seq), k=len(seq))

    mvars = []
    for i in tqdm(range(20), desc="Optimizing number of PCs"):
        randomized = adata.to_df().apply(jumble, axis=0)
        rndata = AnnData(randomized, dtype=adata.X.dtype)
        sc.tl.pca(rndata, svd_solver="arpack")
        mvars.append(rndata.uns["pca"]["variance"][0])

    cutoff = np.mean(mvars)
    sc.tl.pca(adata, svd_solver="arpack")
    n_pcs = int(np.sum(adata.uns["pca"]["variance"] > cutoff))
    stats.set("Number of PCs", n_pcs)
    return n_pcs


def cluster_cells(adata, n_pcs):
    if "pca" not in adata.uns:
        sc.tl.pca(adata, svd_solver="arpack")
    print("Calculating neighbors...", end="")
    sc.pp.neighbors(adata, n_pcs=n_pcs)
    print("done\nLeiden clustering...", end="")
    sc.tl.leiden(adata)
    print("done\nCalculating UMAP...", end="")
    sc.tl.paga(adata)
    sc.pl.paga(adata, plot=False)
    sc.tl.umap(adata, init_pos="paga", min_dist=0.3, spread=1)
    print("done")
    stats.set("Number of clusters", len(np.unique(adata.obs["leiden"])))
