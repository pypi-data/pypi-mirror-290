"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import numpy as np
import torch
from sklearn.datasets import make_classification
from .util import itemize

HSBLOCKS = np.array([[0, 0],
                     [1, 1]], dtype=np.int32)

VSBLOCKS = np.array([[0, 1],
                     [0, 1]], dtype=np.int32)

CHBLOCKS = np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]], dtype=np.int32)

GGBLOCKS = np.array([[0, 1, 0, 2, 2, 2],
                     [1, 1, 1, 2, 0, 2],
                     [0, 1, 0, 2, 2, 2],
                     [3, 0, 0, 4, 4, 4],
                     [3, 3, 0, 0, 4, 0],
                     [3, 3, 3, 0, 4, 0]], dtype=np.int32)

def make_bins(n_samples, n_bins):
    """Apportions samples evenly into bins and returns the number of samples in
    each bin.
    
    Parameters
    ----------
    n_samples : int
        Number of samples.
    n_bins : int
        Number of bins.

    Returns
    -------
    list of shape=(n_bins,)
        Number of samples in each bin.
    """

    parts = [n_samples//n_bins]

    for i in range(1, n_bins):
        parts.append((n_samples - sum(parts))//(n_bins - i))
        
    return parts

def make_features(n_features, n_components, n_equivocal=0, n_redundant=0, mean_scale=1., variance_scale=1.):
    """Generates unique mean values for each feature in each component and 
    unique variance values for each feature.
    
    Parameters
    ----------
    n_features : int
        Number of features per sample.
    n_components : int
        Number of components.
    n_equivocal : int, default=0
        Number of equivocal features.
    n_redundant : int, default=0
        Number of redundant features.
    mean_scale : float, default=1.0
        Mean value multiplier.
    variance_scale : float, default=1.0
        Variance value multiplier.

    Returns
    -------
    ndarray of shape=(n_components, n_features)
        Mean values for each feature in each component.
    ndarray of shape=(n_features,)
        Variance values for each feature.
    """
    
    n_informative = n_features - n_equivocal - n_redundant
    means, _ = make_classification(n_samples=n_components, n_features=n_features, n_informative=n_informative, n_redundant=n_redundant, n_classes=n_components, n_clusters_per_class=1, scale=mean_scale)
    variances = variance_scale*np.random.rand(n_features)

    return means, variances

def make_components(n_samples, n_features, n_components, n_equivocal=0, n_redundant=0, sample_counts=None, means=None, variances=None, mean_scale=1., variance_scale=1.):
    """Apportions samples evenly into components with unique feature
    parameterizations.
    
    Parameters
    ----------
    n_samples : int
        Number of samples.
    n_features : int
        Number of features per sample.
    n_components : int
        Number of components.
    n_equivocal : int, default=0
        Number of equivocal features.
    n_redundant : int, default=0
        Number of redundant features.
    sample_counts : tuple of shape=(n_components,), default=None
        Number of samples in each component.
    means : ndarray of shape=(n_components, n_features), default=None
        Mean values for each feature in each component.
    variances : ndarray of shape=(n_features,), default=None
        Variance values for each feature.
    mean_scale : float, default=1.0
        Mean value multiplier.
    variance_scale : float, default=1.0
        Variance value multiplier.

    Returns
    -------
    list of shape=(n_components,)
        Number of samples in each bin.
    ndarray of shape=(n_components, n_features)
        Mean values for each feature in each component.
    ndarray of shape=(n_features,)
        Variance values for each feature.
    """
    
    if sample_counts is None:
        sample_counts = make_bins(n_samples, n_components)

    if means is None:
        means, _ = make_features(n_features, n_components, n_equivocal, n_redundant, mean_scale, variance_scale)

    if variances is None:
        _, variances = make_features(n_features, n_components, n_equivocal, n_redundant, mean_scale, variance_scale)

    return sample_counts, means, variances

def make_samples(n_samples, n_features, n_components, means, variances, component, n_mix=0):
    """Generates sample features and labels for a single component based on its
    feature parameterization.
    
    Parameters
    ----------
    n_samples : int
        Number of component samples.
    n_features : int
        Number of features per sample.
    n_components : int
        Number of components.
    means : ndarray of shape=(n_components, n_features)
        Mean values for each feature in each component.
    variances : ndarray of shape=(n_features,)
        Variance values for each feature.
    component : int
        Component index.
    n_mix : int, default=0
        Number of samples to generate from other components.

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        Component sample data.
    ndarray of shape=(n_samples,)
        Component sample labels.
    """
    
    labels = component*np.ones(n_samples, dtype=np.int32)
    data = np.random.normal(means[component], variances, (n_samples, n_features))
    mix_idx = np.random.randint(0, n_samples, n_mix)
    labels[mix_idx] = np.random.randint(0, n_components, n_mix)
    data[mix_idx] = np.random.normal(means[labels[mix_idx]], variances, (n_mix, n_features))
    
    return data, labels

def transfigure_blocks(blocks):
    """Returns a block dataset palette based on its name.
    
    Parameters
    ----------
    blocks : str
        Block dataset name.

    Returns
    -------
    ndarray of shape=(y_dim, x_dim)
        Block dataset palette.

    Raises
    ------
    NotImplementedError
        If the specified block dataset is not supported.
    """

    if isinstance(blocks, str):
        if blocks == 'hsblocks':
            return HSBLOCKS
        if blocks == 'vsblocks':
            return VSBLOCKS
        if blocks == 'chblocks':
            return CHBLOCKS
        if blocks == 'ggblocks':
            return GGBLOCKS
    
        raise NotImplementedError(f'Block palette "{blocks}" not supported.')
    
    return blocks

def interpret_blocks(blocks, share_components=False):  
    """Returns a list of generated block datasets based on their palettes.
    
    Parameters
    ----------
    blocks : tuple | list of shape=(n_blocks,)
        Block dataset palettes.
    share_components : bool, default=False
        Whether to share components among datasets.

    Returns
    -------
    list of shape=(n_blocks,)
        List of block datasets.
    int
        Number of components across all datasets.
    """

    n_components = []

    for idx, b in enumerate(blocks):
        blocks[idx] = b = transfigure_blocks(b)
        n_components.append(np.unique(b).shape[0])

    n_components = max(n_components) if share_components else sum(n_components)

    return blocks, n_components

def make_data(n_samples, n_features, n_components, n_equivocal=0, n_redundant=0, sample_counts=None, means=None, variances=None, mean_scale=1., variance_scale=1., mix=0.):
    """Generates sample features and labels for all components based on their
    feature parameterizations.
    
    Parameters
    ----------
    n_samples : int
        Number of samples.
    n_features : int
        Number of features per sample.
    n_components : int
        Number of components.
    n_equivocal : int, default=0
        Number of equivocal features.
    n_redundant : int, default=0
        Number of redundant features.
    sample_counts : tuple of shape=(n_components), default=None
        Number of samples in each component.
    means : ndarray of shape=(n_components, n_features), default=None
        Mean values for each feature in each component.
    variances : ndarray of shape=(n_features,), default=None
        Variance values for each feature.
    mean_scale : float, default=1.0
        Mean value multiplier.
    variance_scale : float, default=1.0
        Variance value multiplier.
    mix : float, default=0.0
        Proportion of samples mixed between components.

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        Sample data.
    ndarray of shape=(n_samples,)
        Sample labels.
    """
    
    n_mix = make_bins(int(mix*n_samples), n_components)
    sample_counts, means, variances = make_components(n_samples, n_features, n_components, n_equivocal, n_redundant, sample_counts, means, variances, mean_scale, variance_scale)
    data = np.zeros((n_samples, n_features), dtype=np.float32)
    labels = np.zeros(n_samples, dtype=np.int32)
    j = 0

    for i in range(n_components):
        k = j + sample_counts[i]
        data[j:k], labels[j:k] = make_samples(sample_counts[i], n_features, n_components, means, variances, i, n_mix[i])
        j += sample_counts[i]

    return data, labels

def make_blocks(blocks, n_features, n_equivocal=0, n_redundant=0, means=None, variances=None, mean_scale=1., variance_scale=1., block_size=5, wiggle=0., mix=0.):
    """Generates sample blocks and labels based on a block palette.
    
    Parameters
    ----------
    blocks : ndarray of shape=(y_dim, x_dim)
        Block palette.
    n_features : int
        Number of features per sample.
    n_equivocal : int, default=0
        Number of equivocal features.
    n_redundant : int, default=0
        Number of redundant features.
    means : ndarray of shape=(n_components, n_features), default=None
        Mean values for each feature in each component.
    variances : ndarray of shape=(n_features,), default=None
        Variance values for each feature.
    mean_scale : float, default=1.0
        Mean value multiplier.
    variance_scale : float, default=1.0
        Variance value multiplier.
    block_size : int, default=5
        Size of each block.
    wiggle : float, default=0.0
        Proportion of spatial noise in each sample.
    mix : float, default=0.0
        Proportion of samples mixed between components.

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        Sample block data.
    ndarray of shape=(n_samples,)
        Sample block labels.
    """
    
    grid = np.repeat(np.repeat(blocks, block_size, 0), block_size, 1)
    n_samples = grid.shape[0]*grid.shape[1]
    _, sample_counts = np.unique(grid, return_counts=True)
    n_components = sample_counts.shape[0]
    data, labels = make_data(n_samples, n_features, n_components, n_equivocal, n_redundant, sample_counts, means, variances, mean_scale, variance_scale, mix)
    data = np.hstack([np.zeros((data.shape[0], 2)), data])
    j = 0

    for i in range(n_components):
        locs = np.stack(np.where(grid.T == i)).T
        locs[:, -1] = -locs[:, -1] + grid.shape[0]
        data[j:j + locs.shape[0], :2] = locs
        j += locs.shape[0]

    data[:, :2] += 2*wiggle*np.random.rand(*data[:, :2].shape) - wiggle
    
    return data, labels

def make_dataset(blocks, n_features, n_equivocal=0, n_redundant=0, block_size=5, wiggle=0., mix=0., img=None, offset=0, mean_scale=1., variance_scale=1., means=None, variances=None, return_tensor=False):
    """Generates a sample dataset based on a block name or palette.
    
    Parameters
    ----------
    blocks : str | ndarray of shape=(y_dim, x_dim)
        Block name or palette.
    n_features : int
        Number of features per sample.
    n_equivocal : int, default=0
        Number of equivocal features.
    n_redundant : int, default=0
        Number of redundant features.
    block_size : int, default=5
        Size of each block.
    wiggle : float, default=0.0
        Proportion of spatial noise in each sample.
    mix : float, default=0.0
        Proportion of sample mixed between components.
    img : int, default=None
        Image index.
    offset : int, default=0
        Label offset.
    mean_scale : float, default=1.0
        Mean value multiplier.
    variance_scale : float, default=1.0
        Variance value multiplier.
    means : ndarray of shape=(n_components, n_features), default=None
        Mean values for each feature in each component.
    variances : ndarray of shape=(n_features,), default=None
        Variance values for each feature.
    return_tensor : bool, default=False
        Whether to return a Tensor instead of an ndarray.

    Returns
    -------
    ndarray | Tensor of shape=(n_samples, n_features)
        Sample dataset.
    ndarray | Tensor of shape=(n_samples,)
        Sample labels.
    """

    if means is not None:
        means = means[offset:]
    
    blocks = transfigure_blocks(blocks)
    data, labels = make_blocks(blocks, n_features, n_equivocal, n_redundant, means, variances, mean_scale, variance_scale, block_size, wiggle, mix)
    labels += offset

    if img is not None:
        data = np.hstack([img*np.ones((data.shape[0], 1)), data])

    if return_tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels

def make_datasets(blocks, n_features, n_equivocal=0, n_redundant=0, block_size=5, wiggle=0., mix=0., mean_scale=1., variance_scale=1., means=None, variances=None, share_components=True, return_tensor=False):
    """Generates sample datasets based on a list of block names or palettes.
    
    Parameters
    ----------
    blocks : str | list of shape=(n_datasets,)
        List of block names or palettes.
    n_features : int
        Number of features per sample.
    n_equivocal : int, default=0
        Number of equivocal features.
    n_redundant : int, default=0
        Number of redundant features.
    block_size : int | list of shape=(n_datasets,), default=5
        Size of each block.
    wiggle : float | list of shape=(n_datasets,), default=0.0
        Proportion of spatial noise in each sample.
    mix : float | list of shape=(n_datasets,), default=0.0
        Proportion of samples mixed between components.
    mean_scale : float, default=1.0
        Mean values multiplier.
    variance_scale : float, default=1.0
        Variance values multiplier.
    means : ndarray of shape=(n_components, n_features), default=None
        Mean values for each feature in each component.
    variances : ndarray of shape=(n_features,), default=None
        Variance values for each feature.
    share_components : bool, default=True
        Whether to share components among datasets.
    return_tensor : bool, default=False
        Whether to return a Tensor instead of an ndarray.

    Returns
    -------
    ndarray | Tensor of shape=(n_samples, n_features)
        Sample datasets.
    ndarray | Tensor of shape=(n_samples,)
        Sample labels.
    """
    
    n_datasets = len(blocks) if isinstance(blocks, (tuple, list)) else 1
    blocks, block_size, wiggle, mix = itemize(n_datasets, blocks, block_size, wiggle, mix)
    blocks, n_components = interpret_blocks(blocks, share_components)
    _, means, variances = make_components(1, n_features, n_components, n_equivocal, n_redundant, 1, means, variances, mean_scale, variance_scale)
    datasets = []

    for idx, (b, s, w, m) in enumerate(zip(blocks, block_size, wiggle, mix)):
        offset = 0 if share_components or len(datasets) == 0 else max(datasets[-1][1]) + 1
        datasets.append(make_dataset(b, n_features, n_equivocal, n_redundant, s, w, m, idx, offset, mean_scale, variance_scale, means, variances))

    data, labels = zip(*datasets)
    data = np.concatenate(data)
    labels = np.concatenate(labels)

    if return_tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels
