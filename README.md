# Time-resolved single-cell and spatial gene regulatory atlas of plants under pathogen attack
![Project Banner](images/connections.png)

> [!NOTE]
> In this repository, we show how to reproduce the figures from our 2023 manuscript[^1]. Additionally, we provide our data processing pipelines to create fully-processed Anndata and Seurat objects containing all of the single-cell and spatial data used to construct figures.

## Table of Contents

- [Abstract](#abstract)
- [Setup](#setup)
- [Download](#download)
- [Preprocessing](#preprocessing)
- [Figures](#figures)
- [Submitting changes](#submittingchanges)

## Abstract
Plants lack specialized and mobile immune cells, requiring any cells–regardless of cell type–that encounter pathogens to mount immune responses and communicate with surrounding cells for successful defense. However, the diversity, spatial organization, and function of cellular immune states in pathogen-infected plants are scarcely understood. Here, we comprehensively identify cell states in Arabidopsis thaliana leaves infected by immune-triggering and -suppressive bacterial pathogens by integrating time-resolved single-cell transcriptomics, epigenomics, and spatial transcriptomics. We reveal cell state-specific gene regulatory logic involving transcription factors (TFs), putative cis-regulatory elements, and target genes associated with disease and immunity. We identify a rare cell population that emerges at the nexus of immune-active hotspots designated as the Primary IMmunE Responder (PRIMER) cells. PRIMER cells show non-canonical immune signatures, exemplified by the expression of a previously uncharacterized TF, GT-3a, and high accessibility of this TF in the genome. We demonstrate that GT-3a negatively regulates plant immune responses against bacterial pathogens. PRIMER cells are surrounded by cells that activate genes for long-distance cell-to-cell immune signaling, suggesting potential interactions between these cell states for propagating immune responses across the leaf. Our molecularly defined spatiotemporal atlas serves as a discovery platform for immune cell states with functional and regulatory insights.

## Setup

This repository contains a `devcontainer` to allow to run the scripts in a reproducible manner. Please see the [documentation](https://code.visualstudio.com/docs/devcontainers/containers) for further information on how to use devcontainers.

## Download

The data needed to reproduce our results is available at XXXXXXXXXXXXXX.
To reproduce the main figures, the following files in the `data` directory are needed.

> [!IMPORTANT]
> A script to download the processed data is included [here](download.ipynb).

```text
data
├── segmentations
│   └── kt56
│       ├── segmentation_kt_cell_stats.csv
│       └── segmentation_kt_counts.tsv
├── useful_files
│   └── geneID_to_geneName_MERSCOPE_panel1.txt
```

## Preprocessing

We had two major pipelines in the computational analysis.

1. snMultiome data processing of Arabidopsis time course after infection replicate 1.
   [snMultiome rep 1 processing](/processing_pipelines/snMultiome_replicate_1_processing)
2. snMultiome data processing of Arabidopsis time course after infection replicate 2.
   [snMultiome rep 2 processing](/processing_pipelines/snMultiome_replicate_2_processing)
3. Processing of MERSCOPE Arabidosis time course after infection.
   [MERSCOPE processing](/processing_pipelines/MERSCOPE_processing)

## Figures

This section contains the scripts to reproduce the figures in the paper.

### Figure 1

| Figure | Link                                                  |
|--------|-------------------------------------------------------|
| 1b     | [Notebook](/Figure_1/1b.ipynb)         |
| 1c     | [Notebook](/Figure_1/1c.ipynb) |
| 1d     | [Notebook](/Figure_1/1d.ipynb)                  |

### Figure 2

| Figure                 | Link                                                |
|------------------------|-----------------------------------------------------|
| 2a <br /> 2b <br /> 2c | [Notebook](/Figure_2/2abc.ipynb) |
| 2d                     | [Notebook](/Figure_2/2d.ipynb)                   |
| 2e <br /> 2f           | [Notebook](/Figure_2/2ef.ipynb)   |
| 2g                     | [Notebook](/Figure_2/2g.ipynb)  |
| 2h <br /> 2i           | [Notebook](/Figure_2/2hi.ipynb)       |
| 2j                     | [Notebook](/Figure_2/2j.ipynb)         |

### Figure 3

| Figure       | Link                                                                                                                                                                                  |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 3a           | [Notebook](/Figure_3/3a.ipynb)                                                                                                                            |
| 3b <br /> 3c | [Notebook](/Figure_3/3bc.ipynb)                                                                                                                       |
| 3d           | [Notebook](/Figure_3/3d.ipynb)                                                                                                                       |
| 3e           | [Notebook](/Figure_3/3e.ipynb)                                                                                                                            |
| 3f           | [Notebook](/Figure_3/3f.ipynb)                                                                                                                           |
| 3g           | Cellchat <br /> [Notebook](/Figure_3/3g_part1.ipynb) <br /> [Notebook](/Figure_3/3g_part2.ipynb) <br /> [Notebook](/Figure_3/3g_part3.ipynb) |

### Figure 4

| Figure       | Link                                                          |
|--------------|---------------------------------------------------------------|
| 4a           | [Notebook](/Figure_4/4a.ipynb)                          |
| 4b <br /> 4e | [Notebook](/Figure_4/4be.ipynb)               |
| 4d           | [Notebook](/Figure_4/4d.ipynb)          |
| 4g <br /> 4h | [Notebook](/Figure_4/4gh.ipynb) |

### Figure 5

| Figure       | Link                                                                                                                                                                                                                                                                                                                                                 |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 5a <br /> 5b | [Notebook](/Figure_5/5ab.ipynb)                                                                                                                                                                                                                                                                                                 |
| 5c           | [Notebook](/Figure_5/5c.ipynb)                                                                                                                                                                                                                                                                                                |
| 5d           | [Notebook](/Figure_5/5d.ipynb)                                                                                                                                                                                                                                                                                                  |
| 5e <br /> 5f | [Notebook](/Figure_5/5ef.ipynb)                                                                                                                                                                                                                                                                                                  |
| 5g           | [Notebook](/Figure_5/5g.ipynb)                                                                                                                                                                                                                                                                             |
| 5h           | Cellchat <br /> [Notebook](/Figure_5/5h_part1_dataset_export_signature.ipynb) <br /> [Notebook](/Figure_5/5h_part2_cellchat_preparation%20signature.ipynb) <br /> [Notebook](/Figure_5/5h_part3_spatial_cellchat_signature.ipynb) <br /> [Notebook](/Figure_5/5h_part4_output_cellchat.ipynb) |

### Extended data figures

| Figure             | Link                                 |
|--------------------|--------------------------------------|
| ED 2b              | [Notebook](/Figure_2/2g.ipynb)       |
| ED 2d              | [Notebook](/Figure_2/2j.ipynb)       |
| ED 3d              | [Notebook](/Figure_3/3g_part3.ipynb) |
| ED 4a              | [Notebook](/Figure_3/3g_part3.ipynb) |
| ED 4f              | [Notebook](/Figure_4/4be.ipynb)      |
| ED 5b <br /> ED 5d | [Notebook](/Figure_5/5ab.ipynb)      |

## Submitting changes

> [!IMPORTANT]
> Make sure to run `pre-commit run --all-files` before commiting

## Contact

- Tatsuya Nobori: :envelope: tnobori@salk.edu
- Alexander Monell: :envelope: amonell@ucsd.edu
- Joe Ecker: :envelope: ecker@salk.edu

[^1]: https://www.biorxiv.org/content/10.1101/2023.04.10.536170v1
