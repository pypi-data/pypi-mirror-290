import os
import pytest
import sys
import torch
import torch.nn as nn
from torch.optim import Optimizer
from torch.utils.data import DataLoader
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scelda.nets import activation, layer, mlp, Encoder, Decoder, MLP, VAE

def test_activation_return(act='relu'):
    test_act = activation(act)
    assert isinstance(test_act, nn.ReLU)

def test_activation_raise(act='test'):
    with pytest.raises(NotImplementedError):
        activation(act)

def test_layer(n_samples=1000, n_features=15, input_dim=15, output_dim=5):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = nn.Sequential(*list(layer(input_dim, output_dim)))
    output = model(input)
    assert output.shape == (n_samples, output_dim)

def test_mlp(n_samples=1000, n_features=15, layers=(15, 10, 5)):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = nn.Sequential(*list(mlp(layers)))
    output = model(input)
    assert output.shape == (n_samples, layers[-1])

def test_MLP_forward(n_samples=1000, n_features=15, layers=(15, 10, 5)):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = MLP(layers)
    output = model(input)
    assert output.shape == (n_samples, layers[-1])

def test_Encoder_forward(n_samples=1000, n_features=15, layers=(15, 10, 5)):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = Encoder(layers)
    mean, variance = model(input)
    assert mean.shape == variance.shape == (n_samples, layers[-1])

def test_Decoder_forward(n_samples=1000, n_features=5, layers=(5, 10, 15)):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = Decoder(layers)
    output = model(input)
    assert output.shape == (n_samples, layers[-1])

def test_VAE_build(n_samples=1000, n_features=15, layers=(15, 10, 5), test_size=.2):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = VAE(layers)
    train_loader, test_loader = model.build(input, test_size=test_size)
    assert train_loader.dataset.shape == (int(n_samples*(1. - test_size)), n_features)
    assert test_loader.dataset.shape == (int(n_samples*test_size), n_features)
    assert isinstance(model.encoder, nn.Module)
    assert isinstance(model.decoder, nn.Module)
    assert isinstance(model.optimizer, Optimizer)

def test_VAE_forward(n_samples=1000, n_features=15, layers=(15, 10, 5)):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = VAE(layers)
    model.build(input)
    output, divergence = model(input, return_divergence=True)
    assert output.shape == (n_samples, layers[-1])
    assert divergence >= 0.

def test_VAE_step(n_samples=1000, n_features=15, layers=(15, 10, 5)):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = VAE(layers)
    loader, _ = model.build(input, test_size=0.)
    loss = model.step(loader, False)
    assert loss >= 0.

def test_VAE_fit(n_samples=1000, n_features=15, layers=(15, 10, 5), n_steps=10, test_rate=1):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = VAE(layers).fit(input, n_steps)
    assert len(model.train_log) == n_steps
    assert len(model.test_log) == n_steps//test_rate

def test_VAE_transform(n_samples=1000, n_features=15, layers=(15, 10, 5), n_steps=10):
    input = torch.arange(n_samples*n_features, dtype=torch.float32).reshape(n_samples, n_features)/(n_samples*n_features)
    model = VAE(layers).fit(input, n_steps)
    output = model.transform(input)
    assert output.shape == (n_samples, layers[-1])
