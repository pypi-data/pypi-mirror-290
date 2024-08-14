"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import torch
import torch.nn as nn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm
from .util import set_seed

def activation(act='relu', **kwargs):
    """Instantiates and returns a torch.nn activation object.
    
    Parameters
    ----------
    act : str, default='relu'
        Activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    kwargs : dict, optional
        Activation object instantiation arguments.

    Returns
    -------
    Module
        Instantiated activation object.

    Raises
    ------
    NotImplementedError
        If the specified activation function is not supported.
    """
    
    if act == 'relu':
        return nn.ReLU(**kwargs)
    elif act == 'softplus':
        return nn.Softplus(**kwargs)
    elif act == 'sigmoid':
        return nn.Sigmoid(**kwargs)
    elif act == 'tanh':
        return nn.Tanh(**kwargs)
    
    raise NotImplementedError(f'Activation "{act}" not supported.')

def layer(input_dim, output_dim, bias=True, act='relu', batch_norm=False, dropout=0.):
    """Constructs a neural network layer with optional batch normalization, 
    activation, and dropout.
    
    Parameters
    ----------
    input_dim : int
        Input dimensionality.
    output_dim : int
        Output dimensionality.
    bias : bool, default=True
        Whether to include a bias term.
    act : str, default='relu'
        Activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    batch_norm : bool, default=False
        Whether to include batch normalization.
    dropout : float, default=0.0
        Amount of dropout.

    Yields
    ------
    Module
        Neural network layer components.
    """
    
    yield nn.Linear(input_dim, output_dim, bias=bias)

    if batch_norm:
        yield nn.BatchNorm1d(output_dim)

    if act is not None:
        yield activation(act)

    if dropout > 0.:
        yield nn.Dropout(dropout)

def mlp(layers, bias=True, act='relu', final_act=None, batch_norm=False, final_norm=False, dropout=0., final_drop=0.):
    """Constructs a multilayer perceptron with optional batch normalizations,
    activations, and dropouts.
    
    Parameters
    ----------
    layers : tuple | list of shape=(n_layers,)
        Layer dimensionalities.
    bias : bool, default=True
        Whether to include bias terms.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    final_act : str, default=None
        Final activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    batch_norm : bool, default=False
        Whether to include hidden batch normalization.
    final_norm : bool, default=False
        Whether to include final batch normalization.
    dropout : float, default=0.0
        Amount of hidden dropout.
    final_drop : float, default=0.0
        Amount of final dropout.

    Yields
    ------
    Module
        Neural network layers.
    """
    
    n_layers = len(layers)

    for i in range(1, n_layers):
        if i < n_layers - 1:
            yield from layer(layers[i - 1], layers[i], bias, act, batch_norm, dropout)
        else:
            yield from layer(layers[i - 1], layers[i], bias, final_act, final_norm, final_drop)

class MLP(nn.Module):
    """Implementation of a multilayer perceptron.
    
    Parameters
    ----------
    layers : tuple | list of shape=(n_layers,)
        Layer dimensionalities.
    bias : bool, default=True
        Whether to include bias terms.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    final_act : str, default=None
        Final activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    batch_norm : bool, default=False
        Whether to include hidden batch normalization.
    final_norm : bool, default=False
        Whether to include final batch normalization.
    dropout : float, default=0.0
        Amount of hidden dropout.
    final_drop : bool, default=0.0
        Amount of final dropout.

    Attributes
    ----------
    net : Sequential
        Neural network model.

    Usage
    -----
    >>> layers = (100, 250, 100)
    >>> mlp = MLP(layers, **kwargs)
    >>> output = mlp(input)
    """
    
    def __init__(self, layers, bias=True, act='relu', final_act=None, batch_norm=False, final_norm=False, dropout=0., final_drop=0.):
        super().__init__()

        self.net = nn.Sequential(*list(mlp(layers, bias, act, final_act, batch_norm, final_norm, dropout, final_drop)))

    def forward(self, x):
        """Performs a single forward pass of the network and returns the 
        computed output.
        
        Parameters
        ----------
        x : Tensor of shape=(n_samples, input_dim)
            Network input.

        Returns
        -------
        Tensor of shape=(n_samples, output_dim)
            Network output.
        """
        
        y = self.net(x)

        return y
    
class Encoder(nn.Module):
    """Implementation of a variational neural network encoder.
    
    Parameters
    ----------
    layers : tuple | list of shape=(n_layers,)
        Layer dimensionalities.
    bias : bool, default=True
        Whether to include bias terms.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    final_act : str, default='relu'
        Final activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    batch_norm : bool, default=False
        Whether to include hidden batch normalization.
    final_norm : bool, default=False
        Whether to include final batch normalization.
    dropout : float, default=0.0
        Amount of hidden dropout.
    final_drop : float, default=0.0
        Amount of final dropout.

    Attributes
    ----------
    e_net : MLP
        Reduction network.
    m_net : MLP
        Mean encoder network.
    v_net : MLP
        Variance encoder network.

    Usage
    -----
    >>> layers = (100, 50, 25)
    >>> encoder = Encoder(layers, **kwargs)
    >>> encoding = encoder(data)
    """
    
    def __init__(self, layers, bias=True, act='relu', final_act='relu', batch_norm=False, final_norm=False, dropout=0., final_drop=0.):
        super().__init__()

        self.e_net = MLP(layers[:-1], bias, act, final_act, batch_norm, final_norm, dropout, final_drop)
        self.m_net = MLP(layers[-2:], bias, act, final_act=None, batch_norm=batch_norm, dropout=dropout)
        self.v_net = MLP(layers[-2:], bias, act, final_act=None, batch_norm=batch_norm, dropout=dropout)

    def forward(self, x):
        """Performs a single forward pass of the network and returns the
        encoded mean and variance.

        Parameters
        ----------
        x : Tensor of shape=(n_samples, input_dim)
            Sample dataset.

        Returns
        -------
        m : Tensor of shape=(n_samples, output_dim)
            Encoded mean for each sample.
        v : Tensor of shape=(n_samples, output_dim)
            Encoded variance for each sample.
        """
        
        e = self.e_net(x)
        m = self.m_net(e)
        v = self.v_net(e).exp()

        return m, v
    
class Decoder(nn.Module):
    """Implementation of a neural network decoder.

    Parameters
    ----------
    layers : tuple | list of shape=(n_layers,)
        Layer dimensionalities.
    bias : bool, default=True
        Whether to include bias terms.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    final_act : str, default=None
        Final activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    batch_norm : bool, default=False
        Whether to include hidden batch normalization.
    final_norm : bool, default=False
        Whether to include final batch normalization.
    dropout : float, default=0.0
        Amount of hidden dropout.
    final_drop : float, default=0.0
        Amount of final dropout.

    Attributes
    ----------
    d_net : MLP
        Reconstruction network.

    Usage
    -----
    >>> layers = (25, 50, 100)
    >>> decoder = Decoder(layers, **kwargs)
    >>> decoding = decoder(encoding)
    """
    
    def __init__(self, layers, bias=True, act='relu', final_act=None, batch_norm=False, final_norm=False, dropout=0., final_drop=0.):
        super().__init__()

        self.d_net = MLP(layers, bias, act, final_act, batch_norm, final_norm, dropout, final_drop)

    def forward(self, z):
        """Performs a single forward pass of the network and returns the 
        decoded reconstruction.
        
        Parameters
        ----------
        z : Tensor of shape=(n_samples, input_dim)
            Encoded dataset.
        
        Returns
        -------
        Tensor of shape=(n_samples, output_dim)
            Decoded dataset.
        """
        
        d = self.d_net(z)

        return d
    
class VAE(nn.Module, BaseEstimator, TransformerMixin):
    """Implementation of a variational autoencoder based on the methods proposed
    by Diederik P. Kingma and Max Welling.

    https://arxiv.org/abs/1312.6114
    
    Parameters
    ----------
    layers : tuple | list of shape=(n_layers,)
        Layer dimensionalities.
    bias : bool, default=True
        Whether to include bias terms.
    act : str, default='relu'
        Hidden activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    encoder_act : str, default='relu'
        Encoder activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    decoder_act : str, default=None
        Decoder activation function.
        Supports 'relu', 'softplus', 'sigmoid', and 'tanh'.
    batch_norm : bool, default=True
        Whether to include hidden batch normalization.
    final_norm : bool, default=False
        Whether to include final batch normalization.
    dropout : float, default=0.2
        Amount of hidden dropout.
    final_drop : float, default=0.0
        Amount of final dropout.
    divergence : float, default=0.1
        KL divergence multiplier.
    seed : int, default=None
        Random state seed.

    Attributes
    ----------
    encoder : Encoder
        Encoder network.
    decoder : Decoder
        Decoder network.
    train_log : list of shape=(n_steps,)
        Record of the total loss + KL divergence at each train step.
    test_log : list of shape=(n_steps//test_rate,)
        Record of the total loss + KL divergence at each test step.

    Usage
    -----
    >>> model = VAE(**kwargs)
    >>> encoding = model.fit_transform(data, **kwargs)
    """
    
    def __init__(self, layers=(100, 10), bias=True, act='relu', encoder_act='relu', decoder_act=None, batch_norm=True, final_norm=False, dropout=.2, final_drop=0., divergence=.1, seed=None):
        super().__init__()
        set_seed(seed)

        self.layers = layers
        self.bias = bias
        self.act = act
        self.encoder_act = encoder_act
        self.decoder_act = decoder_act
        self.batch_norm = batch_norm
        self.final_norm = final_norm
        self.dropout = dropout
        self.final_drop = final_drop
        self.divergence = divergence
        self.seed = seed

        self.encoder = None
        self.decoder = None
        self.train_log = []
        self.test_log = []

    def build(self, X, learning_rate=1e-2, batch_size=None, test_size=.2):
        """Initializes class attributes based on sample data.
        
        Parameters
        ----------
        X : Tensor of shape=(n_samples, input_dim)
            Sample dataset.
        learning_rate : float, default=0.001
            Training step size.
        batch_size : int, default=None
            Number of samples used in each forward/backward pass.
        test_size : float, default=0.2
            Proportion of samples used to test the model.

        Returns
        -------
        DataLoader
            Iterable over the train dataset.
        DataLoader
            Iterable over the test dataset.
        """
        
        if self.layers[0] != X.shape[-1]:
            self.layers = (X.shape[-1], *self.layers)

        self.encoder = Encoder(self.layers, self.bias, self.act, self.encoder_act, self.batch_norm, self.batch_norm, self.dropout, self.dropout)
        self.decoder = Decoder(self.layers[::-1], self.bias, self.act, self.decoder_act, self.batch_norm, self.final_norm, self.dropout, self.final_drop)
        self.optimizer = Adam(self.parameters(), learning_rate)

        if batch_size is None:
            batch_size = int(X.shape[0]*(1. - test_size))

        if test_size > 0.:
            X_train, X_test = train_test_split(X, test_size=test_size)
            train_loader, test_loader = DataLoader(X_train, batch_size), DataLoader(X_test, batch_size)
        else:
            train_loader, test_loader = DataLoader(X, batch_size), None

        return train_loader, test_loader
    
    def forward(self, x, return_divergence=False):
        """Performs a single forward pass of the encoder network and returns the
        encoding.
        
        Parameters
        ----------
        x : Tensor of shape=(batch_size, input_dim)
            Sample batch.
        return_divergence : bool, default=False
            Whether to return the KL divergence.

        Returns
        -------
        Tensor of shape=(batch_size, latent_dim)
            Encoded representation for each batch sample.
        float
            KL divergence of the encoded samples.
        """

        m, v = self.encoder(x)
        z = m + v*torch.randn_like(v)

        if return_divergence:
            divergence = self.divergence*(m**2 + v**2 - v.log() - .5).sum()

            return z, divergence
        return z

    def backward(self, loss):
        """Performs a single backward pass of the encoder and decoder networks
        and returns the numerical loss value.
        
        Parameters
        ----------
        loss : Tensor of shape=()
            Loss to be propagated backward.
        
        Returns
        -------
        float
            Numerical loss value.
        """
    
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
    
    def step(self, loader, grad=True):
        """Performs a forward and optional backward pass of the encoder and 
        decoder networks for each batch of the sample dataset.

        Parameters
        ----------
        loader : DataLoader
            Iterable over the sample dataset.
        grad : bool, default=True
            Whether to perform a backward pass.

        Returns
        -------
        float
            Cumulative step loss.
        """
        
        step_loss = 0.

        for x in loader:
            z, divergence = self(x, return_divergence=True)
            y = self.decoder(z)
            loss = (y - x).square().sum() + divergence
            step_loss += self.backward(loss) if grad else loss.item()
            
        step_loss /= loader.dataset.shape[0]

        return step_loss
    
    def fit(self, X, n_steps=150, learning_rate=1e-2, batch_size=None, test_size=.2, test_rate=1, desc='VAE', verbosity=1):
        """Learns an encoded representation for each data sample using a 
        variational training procedure.
        
        Parameters
        ----------
        X : Tensor of shape=(n_samples, input_dim)
            Sample dataset.
        n_steps : int, default=100
            Number of training steps.
        learning_rate : float, default=0.001
            Training step size.
        batch_size : int, default=None
            Number of samples used in each forward/backward pass.
        test_size : float, default=0.2
            Proportion of samples used to test the model.
        test_rate : int, default=1
            Number of steps between validation tests.
        desc : str, default='VAE'
            Model description.
        verbosity : int, default=1
            Level of information logging.
            0 : No logging
            1 : Progress logging
            2 : Detailed logging

        Returns
        -------
        self
            I return therefore I am.
        """
        
        train_loader, test_loader = self.build(X, learning_rate, batch_size, test_size)

        for i in tqdm(range(n_steps), desc) if verbosity == 1 else range(n_steps):
            self.train_log.append(self.step(train_loader, grad=True))

            if test_loader is not None and i%test_rate == 0:
                self.test_log.append(self.step(test_loader, grad=False))

        return self
    
    def transform(self, X):
        """Returns the encoded representation for each data sample learned by 
        the encoder network.
        
        Parameters
        ----------
        X : Tensor of shape=(n_samples, input_dim)
            Sample dataset.
        
        Returns
        -------
        Tensor of shape=(n_samples, latent_dim)
            Encoded representation for each data sample.
        """
        
        Z = self(X)

        return Z.detach()
