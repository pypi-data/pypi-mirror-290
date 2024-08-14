"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import matplotlib.pyplot as plt
import muon as mu
import numpy as np
import os
import pyro
import random
import torch
from itertools import product
from matplotlib import cm, colormaps, colors
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

def set_seed(seed=9):
    """Sets a fixed environment-wide random state.

    Parameters
    ----------
    seed : int, default=9
        Random state seed.

    Returns
    -------
    None
    """

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True
        pyro.set_rng_seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)

def sample_grid(param_grid, threshold=.1):
    """Randomly selects parameter sets from a grid of possible values.
    
    Parameters
    ----------
    param_grid : dict
        Grid of possible values for each parameter
    threshold : float, default=0.1
        Probability of selecting each parameter set.

    Returns
    -------
    list of shape=(n_param_sets, n_params)
        Collection of parameter sets.
    """
    
    ranges = [range(0, len(list(param_grid.values())[i])) for i in range(len(param_grid))]
    parameters = []
    
    for range_ in product(*ranges):
        if np.random.rand() < threshold:
            parameters.append({})

            for idx, value in enumerate(range_):
                parameters[-1][list(param_grid.keys())[idx]] = list(param_grid.values())[idx][value]

    return parameters

def autotune(model, data, param_grid, threshold=.1, recall=10, log_id='loss_log', maximize=False, verbosity=0, **kwargs):
    """Selects the optimal parameter set for a semantic segmentation model based
    on its performance on some sample data according to some metric log. 
    
    Parameters
    ----------
    model : SLDA | sceLDA
        Semantic segmentation model.
    data : ndarray | tensor of shape=(n_samples, n_features)
        Sample data.
    param_grid : dict
        Grid of possible values for each parameter.
    threshold : float, default=0.1
        Probability of selecting each parameter set for testing.
    recall : int, default=10
        Number of metric log steps to average.
    log_id : str, default='loss_log'
        Metric log name.
    maximize : bool, default=False
        Whether to maximize the metric log.
    verbosity : int, default=1
        Level of information logging.
        0 : No logging
        1 : Progress logging
        2 : Detailed logging
    kwargs : dict
        Model fit_transform arguments.

    Returns
    -------
    list of shape=(n_parameters,)
        Optimal parameter set.
    """
    
    parameters = sample_grid(param_grid, threshold)

    for parameter_set in tqdm(parameters) if verbosity == 1 else parameters:
        subject = model(**parameter_set)
        subject.fit_transform(data, verbosity=verbosity, **kwargs)
        log = sum(getattr(subject, log_id)[-recall:])/recall

    parameter_idx = np.argmax(log) if maximize else np.argmin(log)
    parameter_set = parameters[parameter_idx]

    return parameter_set
    
def map_labels(X_labels, Y_labels):
    """Maps predicted cluster labels to the given ground truth using linear sum 
    assignment.
    
    Parameters
    ----------
    X_labels : ndarray of shape=(n_samples,)
        Ground truth cluster labels.
    Y_labels : ndarray of shape=(n_samples,)
        Predicted cluster labels.

    Returns
    -------
    ndarray of shape=(n_samples,)
        Aligned labels.
    """

    scores = confusion_matrix(Y_labels, X_labels)
    row, col = linear_sum_assignment(scores, maximize=True)
    labels = np.zeros_like(X_labels)

    for i in row:
        labels[Y_labels == i] = col[i]

    return labels

def get_spatial(mdata, spatial_key='spatial', modality_key='morphological'):
    """Retrieves spatial information for each sample in an annotated data 
    object.
    
    Parameters
    ----------
    mdata : AnnData | MuData
        Annotated data object.
    spatial_key : str, default='spatial'
        Spatial key.
    modality_key : str, default='morphological'
        Modality key.
    
    Returns
    -------
    ndarray of shape=(n_samples, 2)
        Spatial information for each sample.
        Formatted as (x-coordinate, y-coordinate)
    """

    try:
        return mdata[modality_key].obsm[spatial_key].T
    except KeyError:
        return mdata.obsm[spatial_key].T
    
def get_features(mdata, feature_key='protein', imagenet_key='imagenet'):
    """Retrieves feature information for each sample in an annotated data 
    object.

    Parameters
    ----------
    mdata : AnnData | MuData
        Annotated data object.
    feature_key : str, default='protein'
        Feature key.
    imagenet_key : str, default='imagenet'
        Imagenet feature key.
    normalize : bool, default=True
        Whether to perform feature normalization.
    
    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        Feature information for each sample.
    """

    try:
        features = mdata[feature_key].X
    except KeyError:
        features = mdata.X
    features += features.min() if features.min() > 0. else -features.min()
    features /= features.max()

    if imagenet_key:
        imagenet = mdata[imagenet_key].X
        imagenet += imagenet.min() if imagenet.min() > 0. else -imagenet.min()
        imagenet /= imagenet.max()
        features = np.hstack([features, imagenet])

    return features
    
def get_labels(mdata, label_key='celltype', modality_key='protein'):
    """Retrieves label information for each sample in an annotated data object.
    
    Parameters
    ----------
    mdata : AnnData | MuData
        Annotated data object.
    label_key : str, default='celltype'
        Label key.
    modality_key : str, default='protein'
        Modality key.

    Returns
    -------
    ndarray of shape=(n_samples,)
        Label information for each sample.
    """
    
    try:
        labels = mdata[modality_key].obs[label_key]
    except KeyError:
        labels = mdata.obs[label_key]

    return labels

def remove_lonely(data, labels, n_neighbors=12, threshold=225.):
    """Filters out samples that are spatially removed from the sample data of 
    interest.

    Parameters
    ----------
    data : ndarray of shape=(n_samples, n_features)
        Sample data.
    labels : array-like of shape=(n_samples,)
        Sample labels.
    n_neighbors : int, default=12
        Number of sample neighbors.
    threshold : float, default=225.0
        Maximum neighbor distance.

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        Filtered sample data.
    ndarray of shape=(n_samples,)
        Filtered sample labels.
    """

    knn = NearestNeighbors(n_neighbors=n_neighbors).fit(data[:, :2])
    max_dist = knn.kneighbors()[0].max(-1)
    mask_idx, = np.where(max_dist > threshold)
    data = np.delete(data, mask_idx, axis=0)
    labels = np.delete(labels, mask_idx, axis=0)

    return data, labels

def read_anndata(name, spatial_key='spatial', spatial_modality='morphological', feature_key='protein', imagenet_key='imagenet', label_key='celltype', label_modality='protein', n_neighbors=12, threshold=225., delineate=False, return_tensor=False):
    """Reads sample data and labels from an annotated data object file and 
    returns them as ndarrays.
    
    Parameters
    ----------
    name : str
        Annotated data object file name.
    spatial_key : str, default='spatial'
        Spatial key.
    spatial_modality : str, default='morphological'
        Spatial modality key.
    feature_key : str, default='protein'
        Feature key.
    imagenet_key : str, default='imagenet'
        Imagenet feature key.
    label_key : str, default='celltype'
        Label key.
    label_modality : str, default='protein'
        Label modality key.
    n_neighbors : int, default=12
        Number of sample neighbors.
    threshold : float, default=225.0
        Maximum neighbor distance.
    delineate : bool, default=False
        Whether to include an image index column.
    return_tensor : bool, default=False
        Whether to return a Tensor instead of an ndarray.

    Returns
    -------
    ndarray or tensor of shape=(n_samples, n_features)
        Sample dataset.
    ndarray or tensor of shape=(n_samples,)
        Sample labels.
    """

    mdata = mu.read(name)
    x, y = get_spatial(mdata, spatial_key, spatial_modality)
    features = get_features(mdata, feature_key, imagenet_key)
    data = np.hstack([x[None].T, y[None].T, features])
    labels = get_labels(mdata, label_key, label_modality)
    _, labels = np.unique(labels, return_inverse=True)

    if threshold is not None:
        data, labels = remove_lonely(data, labels, n_neighbors, threshold)

    if delineate:
        data = np.hstack([np.zeros((data.shape[0], 1)), data])

    if return_tensor:
        data, labels = torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels

def read_anndatas(names, spatial_key='spatial', spatial_modality='morphological', feature_key='protein', imagenet_key='imagenet', label_key='celltype', label_modality='protein', n_neighbors=12, threshold=225., return_tensor=False):
    """Read sample data and labels from a list of annotated data object files
    and returns them as ndarrays.
    
    Parameters
    ----------
    names : list
        List of annotated data object file names.
    spatial_key : str, default='spatial'
        Spatial key.
    spatial_modality : str, default='morphological'
        Spatial modality key.
    feature_key : str, default='protein'
        Feature key.
    imagenet_key : str, default='imagenet'
        Imagenet feature key.
    label_key : str, default='celltype'
        Label key.
    label_modality : str, default='protein'
        Label dictionary key.
    n_neighbors : int, default=12
        Number of sample neighbors.
    threshold : float, default=225.0
        Maximum neighbor distance.
    return_tensor : bool, default=False
        Whether to return a Tensor instead of an ndarray.

    Returns
    -------
    ndarray or tensor of shape=(n_samples, n_features)
        Sample datasets.
    ndarray or tensor of shape=(n_samples,)
        Sample labels.
    """

    data, labels = [], []

    for i, name in enumerate(names):
        mdata = mu.read(name)
        x, y = get_spatial(mdata, spatial_key, spatial_modality)
        features = get_features(mdata, feature_key, imagenet_key)
        data_i = np.hstack([x[None].T, y[None].T, features])
        labels_i = get_labels(mdata, label_key, label_modality)
        _, labels_i = np.unique(labels_i, return_inverse=True)

        if threshold is not None:
            data_i, labels_i = remove_lonely(data_i, labels_i, n_neighbors, threshold)

        data.append(np.hstack([i*np.ones((data_i.shape[0], 1)), data_i]))
        labels.append(labels_i)

    data, labels = np.vstack(data), np.hstack(labels)

    if return_tensor:
        data, labels = torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    
    return data, labels

def itemize(n, *items):
    """Converts each item to a list of n identical items.
    
    Parameters
    ----------
    n : int
        Length of item list.
    items : any
        Items to convert to lists.
    
    Yields
    ------
    tuple or list of shape=(n,)
        List of identical items.
    """

    for i in items:
        yield i if isinstance(i, (tuple, list)) else [i,]*n

def format_ax(ax, aspect='equal', show_ax=True):
    """Sets the aspect scaling and axes visiblity of a Matplotlib axis.
    
    Parameters
    ----------
    ax : axis
        Matplotlib axis.
    aspect : str, default='equal'
        Aspect scaling.
    show_ax : bool, default=True
        Whether to show axes.

    Returns
    -------
    axis
        Formatted Matplotlib axis.
    """

    ax.set_aspect(aspect)
    
    if not show_ax:
        ax.axis('off')

    return ax

def show_dataset(locs, labels, size=15, figsize=5, show_ax=False, show_colorbar=False, colormap='Set3', name=None):
    """Displays a scatter plot of sample points colored by label.
    
    Parameters
    ----------
    locs : array-like of shape=(n_samples, 2)
        Sample locations.
        Formatted as (x-coordinate, y-coordinate)
    labels : array-like of shape=(n_samples,)
        Sample labels.
    size : int, default=15
        Sample point size.
    figsize : int, default=10
        Scatter plot size.
    show_ax : bool, default=False
        Whether to show axes.
    show_colorbar : bool, default=False
        Whether to show a colorbar.
    colormap : str, default='Set3'
        Label color dictionary.
    name : str, default=None
        Scatter plot file name.

    Returns
    -------
    None
    """

    cmap = colormaps.get_cmap(colormap)
    norm = colors.Normalize(labels.min(), labels.max())
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(figsize=figsize)
    locs = locs[:, :2].T
    ax.scatter(*locs, s=size, c=cmap(norm(labels)))
    ax = format_ax(ax, aspect='equal', show_ax=show_ax)

    if show_colorbar:
        fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm))

    if name is not None:
        fig.savefig(name, bbox_inches='tight', transparent=True)

def show_datasets(locs, labels, size=15, figsize=10, show_ax=False, show_colorbar=False, colormap='Set3', name=None):
    """Displays scatter plots of sample points colored by label and separated by
    image.
    
    Parameters
    ----------
    locs : array-like of shape=(n_samples, 3)
        Sample locations.
        Formatted as (image, x-coordinate, y-coordinate)
    labels : array-like of shape=(n_samples,)
        Sample labels.
    size : int, default=15
        Sample point size.
    figsize : int, default=10
        Scatter plot size.
    show_ax : bool, default=False
        Whether to show axes.
    show_colorbar : bool, default=False
        Whether to show a colorbar.
    colormap : str, default='Set3'
        Label color dictionary.
    name : str, default=None
        Scatter plot file name.

    Returns
    -------
    None
    """
    
    cmap = colormaps.get_cmap(colormap)
    norm = colors.Normalize(labels.min(), labels.max())
    n_datasets = np.unique(locs[:, 0]).shape[0]
    size, = itemize(n_datasets, size)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_datasets, figsize=figsize)
    axes = (ax,) if n_datasets == 1 else ax

    for i in range(n_datasets):
        idx = locs[:, 0].astype(np.int32) == i
        idx_locs = locs[idx, 1:3].T
        axes[i].scatter(*idx_locs, s=size[i], c=cmap(norm(labels[idx])))
        format_ax(axes[i], aspect='equal', show_ax=show_ax)

    if show_colorbar:
        fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm))

    if name is not None:
        fig.savefig(name, bbox_inches='tight', transparent=True)

def show_logs(logs, figsize=5, show_ax=True, name=None):
    """Displays line plots of log of numerical values.
    
    Parameters
    ----------
    logs : dict
        Dictionary of log titles and values.
    figsize : int, default=10
        Line plot size.
    show_ax : bool, default=True
        Whether to show axes.
    name : str, default=None
        Line plot file name.

    Returns
    -------
    None
    """

    n_logs = len(logs)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_logs, figsize=figsize)
    axes = (ax,) if n_logs == 1 else ax

    for idx, (key, value) in enumerate(logs.items()):
        axes[idx].set_title(key)
        x = np.arange(len(value))
        axes[idx].plot(x, value)
        axes[idx].set_box_aspect(1)

        if not show_ax:
            axes[idx].tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

    if name is not None:
        fig.savefig(name, bbox_inches='tight')
