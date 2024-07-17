import numpy as np
from scipy.spatial import distance
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from tqdm.notebook import tqdm
import pandas as pd
import scanpy as sc


def calculate_centroid(points):
    """
    Calculate the centroid of a set of points
    :param points: list of points
    :return: centroid
    """
    centroid = np.mean(points, axis=0)
    return centroid.tolist()


def bin_points(spatial_points, bin_size=20):
    """
    Bin spatial points into groups of bin_size

    :param spatial_points: list of spatial points
    :param bin_size: number of points per bin
    :return: list of bins, list of bin centers
    """
    bins = []
    bin_centers = []
    points_copy = spatial_points.copy()
    original_indices = np.arange(len(points_copy))

    with tqdm(total=len(points_copy)) as pbar:
        # while there are still points to bin
        while len(points_copy) >= bin_size:
            bin_center = points_copy[0]
            bin_indices = [0]
            bin_points = [bin_center]
            points_copy = np.delete(points_copy, 0, axis=0)
            original_indices = np.delete(original_indices, 0, axis=0)

            # find the nearest points to the bin center
            distances = distance.cdist([bin_center], points_copy)
            nearest_idx = np.argsort(distances)[0][: bin_size - 1]
            nearest_points = points_copy[nearest_idx]
            nearest_indices = original_indices[nearest_idx]

            # add the nearest points to the bin
            bin_indices.extend(nearest_indices)
            bin_points.extend(nearest_points)
            points_copy = np.delete(points_copy, nearest_idx, axis=0)
            original_indices = np.delete(original_indices, nearest_idx, axis=0)

            bin_center = calculate_centroid(bin_points)

            # add the bin to the list of bins
            bin_centers.append(bin_center)
            bins.append(bin_indices)
            pbar.update(bin_size)

    return bins, bin_centers


def create_grid_bins(spatial_points, n):
    """
    Create a grid of bins for spatial points. This is different than the previous functio, where in this function bins are created by spatial coords, not number of points.

    :param spatial_points: list of spatial points
    :param n: number of bins
    :return: grid of bins, bin centers
    """
    xmin, ymin = np.min(spatial_points, axis=0)
    xmax, ymax = np.max(spatial_points, axis=0)

    xbins = np.linspace(xmin, xmax, n + 1)
    ybins = np.linspace(ymin, ymax, n + 1)

    grid_bins = [[[] for _ in range(n)] for _ in range(n)]
    bin_centers = []

    # create a list of bin centers
    for i in range(n):
        for j in range(n):
            bin_center_x = (xbins[i] + xbins[i + 1]) / 2
            bin_center_y = (ybins[j] + ybins[j + 1]) / 2
            bin_centers.append([bin_center_x, bin_center_y])

    # bin the points
    for point in tqdm(range(len(spatial_points))):

        x, y = spatial_points[point]
        xi = np.searchsorted(xbins, x, side="right") - 1
        yi = np.searchsorted(ybins, y, side="right") - 1

        try:
            grid_bins[xi][yi].append(point)
        except:
            None

    return grid_bins, bin_centers


def display_fovs(merfish, remove_fovs=20, key="Cluster"):
    """
    Display the field of views in the MERFISH data

    :param merfish: MERFISH dataset
    :param remove_fovs: number of FOVs to remove
    :param key: key to color the FOVs
    :return: bin centers
    """
    spatial_points = np.array(
        [merfish.obsm["spatial"][:, 0], merfish.obsm["spatial"][:, 1]]
    ).T
    binned_points, binned_centers = create_grid_bins(spatial_points, remove_fovs)

    mfish = []
    for r in merfish.obs[key].tolist():
        mfish.append(merfish.uns[f"{key}_colors"][r])

    plt.figure(figsize=(10, 10), facecolor="white")
    plt.scatter(
        merfish.obsm["spatial"][:, 0],
        merfish.obsm["spatial"][:, 1],
        c=mfish,
        s=1,
        alpha=0.3,
    )
    for j in range(len(binned_centers)):
        plt.text(
            np.array(binned_centers)[j, 0],
            np.array(binned_centers)[j, 1],
            j,
            fontsize=10,
            color="blue",
        )
    plt.grid(False)
    plt.show()
    return binned_centers


def remove_fovs(merfish, fovs_to_remove, binned_centers, key="Cluster"):
    """
    Remove FOVs from the MERFISH dataset in fovs_to_remove

    :param merfish: MERFISH dataset
    :param fovs_to_remove: list of FOVs to remove
    :param binned_centers: bin centers
    :param key: key to color the FOVs
    :return: MERFISH dataset with FOVs removed
    """

    fov_associated = []
    tree = KDTree(binned_centers)
    # find the nearest bin to each point
    for i_bac in tqdm(range(len(merfish.obsm["spatial"]))):
        distances, neighbors = tree.query(merfish.obsm["spatial"][i_bac], k=1)

        fov_associated.append(neighbors)
    # remove the FOVs that contain points and are not in the removal list.
    merfish = merfish[
        [i for i, e in enumerate(fov_associated) if e not in fovs_to_remove], :
    ]

    sc.pl.embedding(merfish, basis="spatial", color=key)

    return merfish
