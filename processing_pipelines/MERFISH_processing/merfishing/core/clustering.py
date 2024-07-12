import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from anndata import AnnData


def plot_qc_feature(cell_by_gene, cell_meta, control_probes=False):

    qc_info = cell_meta

    if control_probes:
        colors = ["#98FB98", "#E6E6FA", "#ADD8E6", "#FFB6C1", "#FFE4E1"]
        metrics = [
            "transcript_counts",
            "cell_area",
            "nucleus_area",
            "transcript_counts_div_cell_area",
            "control_probe_counts",
        ]
        ncols = 5
    else:
        colors = ["#98FB98", "#E6E6FA", "#ADD8E6", "#FFB6C1"]
        metrics = [
            "transcript_counts",
            "cell_area",
            "nucleus_area",
            "transcript_counts_div_cell_area",
        ]
        ncols = 4

    fig, axes = plt.subplots(
        figsize=(15, 3), dpi=200, ncols=ncols, constrained_layout=True
    )
    # Loop through each axis and create violin and strip plots
    for i, ax in enumerate(axes):
        sns.violinplot(y=qc_info[metrics[i]], color=colors[i], ax=ax)
        sns.stripplot(
            y=qc_info[metrics[i]], jitter=True, color="black", ax=ax, size=0.1
        )
        ax.set_title(metrics[i])  # Set title for each subplot

    # Show the plots
    plt.show()


def qc_before_clustering(
    adata,
    min_transcript_threshold=20,
    max_transcript_threshold=250,
    min_cell_area=1,
    max_cell_area=200,
    min_nucleus_area=1,
    max_nucleus_area=70,
    min_tc_area=0.3,
    max_tc_area=10,
):
    print(f"{len(adata.obs.index)} cells before QC filtering")
    adata = adata[
        (adata.obs["cell_area"] > min_cell_area)
        & (adata.obs["cell_area"] < max_cell_area),
        :,
    ]
    adata = adata[
        (adata.obs["nucleus_area"] > min_nucleus_area)
        & (adata.obs["nucleus_area"] < max_nucleus_area),
        :,
    ]
    adata = adata[
        (adata.obs["transcript_counts"] > min_transcript_threshold)
        & (adata.obs["transcript_counts"] < max_transcript_threshold),
        :,
    ]
    adata = adata[
        (adata.obs["transcript_counts_div_cell_area"] > min_tc_area)
        & (adata.obs["transcript_counts_div_cell_area"] < max_tc_area),
        :,
    ]
    print(f"{len(adata.obs.index)} cells after QC filtering")

    return adata
