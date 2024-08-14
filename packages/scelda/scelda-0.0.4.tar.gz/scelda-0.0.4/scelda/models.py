"""
Craig Fouts (cfouts@nygenome.org)
Sarah Rodwin (srodwin@nygenome.org)
"""

import numpy as np
import pickle
import torch
from scipy import stats
from scipy.cluster.vq import kmeans, vq
from scipy.spatial.distance import cdist
from sklearn.base import BaseEstimator, TransformerMixin
from tqdm import tqdm
from .nets import VAE
from .util import set_seed

def load_slda(name='slda'):
    """Loads a pickled SLDA object from file.
    
    Parameters
    ----------
    name : str, default='slda'
        Pickle file name.

    Returns
    -------
    SLDA
        SLDA instance with loaded attributes.
    """
    
    if name[-4:] != '.pkl':
        name += '.pkl'

    with open(name, 'rb') as f:
        attributes = pickle.load(f)

    model = SLDA()
    model.__dict__ = attributes

    return model

def load_scelda(name='scelda'):
    """Loads a pickled sceLDA object from file.
    
    Parameters
    ----------
    name : str, default='scelda'
        Pickle file name.

    Returns
    -------
    sceLDA
        sceLDA instance with loaded attributes.
    """
    
    if name[-4:] != '.pkl':
        name += '.pkl'
    
    with open(name, 'rb') as f:
        attributes = pickle.load(f)

    model = sceLDA()
    model.__dict__ = attributes

    return model

def featurize(data, scale=1.):
    """Creates features by applying a Gaussian filter followed by a Laplacian of 
    Gaussian filter to sample data.
    
    Parameters
    ----------
    data : ndarray of shape=(n_samples, n_features)
        Sample data.
    scale : float, default=1.0
        Gaussian standard deviation.

    Returns
    -------
    ndarray of shape=(n_samples, n_features)
        Filtered sample features.
    """
    
    imgs = np.unique(data[:, 0])
    features = []

    for img in imgs:
        mask = data[:, 0] == img
        proximity = cdist(data[mask, 1:3], data[mask, 1:3])
        gaussian = np.exp(-(proximity/scale)**2)
        laplacian = np.exp(-(proximity/(2*scale))**2)/(2*np.pi*scale**2)
        features.append(laplacian.T@(gaussian.T@data[mask, 3:]))
    
    features = np.vstack(features)

    return features

def distribute(locs, n_docs=250):
    """Uniformly distributes document locations proximally to sample locations.
    
    Parameters
    ----------
    locs : ndarray of shape=(n_samples, 3)
        Sample locations.
        Formatted as (image, x-coordinate, y-coordinate).
    n_docs : int, default=150
        Number of documents to distribute.

    Returns
    -------
    ndarray of shape=(n_docs, 3)
        Distributed document locations.
        Formatted as (image, x-coordinate, y-coordinate).
    """
    
    n_samples = locs.shape[0]
    mask = np.random.permutation(n_samples)[:n_docs]
    docs = locs[mask]

    return docs

def shuffle(words, n_topics=5, n_docs=250, n_words=15, return_counts=False):
    """Randomly initializes document and topic assignments for each sample.

    Parameters
    ----------
    words : ndarray of shape=(n_samples,)
        Word assignment for each sample.
    n_topics : int, default=5
        Number of possible topics.
    n_docs : int, default=150
        Number of possible documents.
    n_words : int, default=15
        Number of possible words.
    return_counts : bool, default=False
        Whether to return assignment counts.

    Returns
    -------
    ndarray of shape=(n_samples, 1)
        Document assignments.
    ndarray of shape=(n_samples, 1)
        Topic assignments.
    ndarray of shape=(n_docs, n_topics)
        Document assignment counts.
    ndarray of shape=(n_topics, n_words)
        Topic assignment counts.
    """

    n_samples = words.shape[0]
    docs = np.random.choice(n_docs, (n_samples, 1))
    topics = np.random.choice(n_topics, (n_samples, 1))

    if return_counts:
        doc_range, topic_range = np.arange(n_docs), np.arange(n_topics)
        doc_counts = (docs == doc_range).T@np.eye(n_topics)[topics.T[0]]
        topic_counts = (topics == topic_range).T@np.eye(n_words)[words]

        return docs, topics, doc_counts, topic_counts
    return docs, topics

class SLDA(BaseEstimator, TransformerMixin):
    """Implementation of spatial latent Dirichlet allocation based on the
    methods proposed by Wang and Grimson.

    https://papers.nips.cc/paper/3278-spatial-latent-dirichlet-allocation
    
    Parameters
    ----------
    n_topics : int, default=5
        Number of possible topics.
    n_docs : int, default=150
        Number of possible documents.
    n_words : int, default=15
        Number of possible words.
    n_neighbors : int, default=15
        Number of document neighbors
    doc_scale : float, default=2.5
        Size of document neighborhood.
    word_scale : float, default=0.25
        Size of word neighborhood.
    doc_prior : float, default=0.1
        Document distribution prior.
    topic_prior : float, default=0.1
        Topic distribution prior.
    seed : int, default=None
        Random state seed.

    Attributes
    ----------
    corpus : ndarray of shape=(n_samples, 6)
        Spatial location and current assignments for each sample.
        Formatted as (image, x-cordinate, y-coordinate, word, document, topic).
    topics : ndarray of shape=(n_samples, n_steps - burn_in)
        Topic assignment history for each sample.
    doc_locs : ndarray of shape=(n_docs*n_imgs, 3)
        Spatial location of each document.
    doc_scales : ndarray of shape=(n_docs*n_imgs,)
        Size of each document neighborhood.
    doc_counts : ndarray of shape=(n_docs*n_imgs, n_topics)
        Document distributions over topics.
    topic_counts : ndarray of shape=(n_topics, n_words)
        Topic distributions over words.
    likelihood_log : list of shape=(n_steps,)
        Record of the total likelihood computed at each inference step.

    Usage
    -----
    >>> model = SLDA(**kwargs)
    >>> topics = model.fit_transform(data, **kwargs)
    """
    
    def __init__(self, n_topics=5, n_docs=250, n_words=15, n_neighbors=15, doc_scale=2.5, word_scale=.25, doc_prior=.1, topic_prior=.1, seed=None):
        super().__init__()
        set_seed(seed)

        self.n_topics = n_topics
        self.n_docs = n_docs
        self.n_words = n_words
        self.n_neighbors = n_neighbors
        self.doc_scale = doc_scale
        self.word_scale = word_scale
        self.doc_prior = doc_prior
        self.topic_prior = topic_prior
        self.seed = seed

        self.corpus = None
        self.topics = None
        self.doc_locs = None
        self.doc_scales = None
        self.doc_counts = None
        self.topic_counts = None
        self.likelihood_log = []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _featurize(self, data):
        return featurize(data, self.word_scale)
    
    def _distribute(self, locs, n_docs):
        return distribute(locs, n_docs)
    
    def _shuffle(self, words, n_docs):
        return shuffle(words, self.n_topics, n_docs, self.n_words, return_counts=True)

    def save(self, name='slda'):
        """Creates a pickled SLDA object and saves it to file.
        
        Parameters
        ----------
        name : str, default='slda'
            Pickle file name.

        Returns
        -------
        None
        """

        if name[-4:] != '.pkl':
            name += '.pkl'
        
        with open(name, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def build(self, data, n_steps=150, burn_in=50):
        """Initializes class attributes based on sample data.
        
        Parameters
        ----------
        data : ndarray of shape=(n_samples, n_features)
            Sample data.
        n_steps : int, default=150
            Total number of inference steps.
        burn_in : int, default=50
            Number of steps to discard.

        Returns
        -------
        self
            I return therefore I am.
        """
        
        locs, features = data[:, :3], self._featurize(data)
        n_samples, n_docs = locs.shape[0], self.n_docs*np.unique(locs[:, 0]).shape[0]
        self.doc_locs = self._distribute(locs, n_docs)
        self.doc_scales = self.doc_scale*np.sort(cdist(self.doc_locs[:, 1:], locs[:, 1:]))[:, :self.n_neighbors].mean(-1)
        words, _ = vq(features, kmeans(features, self.n_words)[0])
        docs, topics, self.doc_counts, self.topic_counts = self._shuffle(words, n_docs)
        self.corpus = np.hstack([locs, words[None].T, docs, topics])
        self.topics = np.zeros((n_samples, n_steps - burn_in))
        self.topics[:, -1:] = topics

        return self
    
    def decrement(self, word, doc, topic):
        """Decreases document and topic counts corresponding to a sample's word, 
        document, and topic assignments.
        
        Parameters
        ----------
        word : int
            Word assignment.
        doc : int
            Document assignment.
        topic : int
            Topic assignment

        Returns
        -------
        ndarray of shape=(n_docs, n_topics)
            Updated document assignment counts.
        ndarray of shape=(n_topics, n_words)
            Updated topic assignment counts.
        """
        
        self.doc_counts[doc, topic] -= 1
        self.topic_counts[topic, word] -= 1

        return self.doc_counts, self.topic_counts
    
    def increment(self, word, doc, topic):
        """Increases document and topic counts corresponding to a sample's word,
        document, and topic assignments.
        
        Parameters
        ----------
        word : int
            Word assignment.
        doc : int
            Document assignment.
        topic : int
            Topic assignment.

        Returns
        -------
        ndarray of shape=(n_docs, n_topics)
            Updated document assignment counts.
        ndarray of shape=(n_topics, n_words)
            Updated topic assignment counts.
        """

        self.doc_counts[doc, topic] += 1
        self.topic_counts[topic, word] += 1

        return self.doc_counts, self.topic_counts
    
    def sample_doc(self, loc, topic, return_likelihood=False):
        """Samples a new document assignment for a sample based on its spatial 
        location and topic assignment.
        
        Parameters
        ----------
        loc : ndarray of shape=(3,)
            Sample location.
            Formatted as (image, x-coordinate, y-coordinate)
        topic : int
            Topic assignment.
        return_likelihood : bool, default=False
            Whether to return the sample likelihood.

        Returns
        -------
        int
            Sampled document assignment.
        float
            Document sample likelihood.
        """
        
        mask = (self.doc_locs[:, 0] == loc[0]).astype(np.int32)
        doc_probs = np.exp(-((loc[1:] - self.doc_locs[:, 1:])**2).sum(-1)/self.doc_scales**2)
        topic_probs = self.doc_counts[:, topic] + self.doc_prior
        topic_probs /= (self.doc_counts + self.doc_prior).sum(-1)
        probs = mask*doc_probs*topic_probs
        probs /= probs.sum()
        doc = np.random.choice(self.doc_locs.shape[0], p=probs)

        if return_likelihood:
            return doc, probs[doc]
        return doc
    
    def sample_topic(self, word, doc, return_likelihood=False):
        """Samples a new topic assignment for a sample based on its word and 
        document assignments.

        Parameters
        ----------
        word : int
            Word assignment.
        doc : int
            Document assignment.
        return_likelihood : bool, default=False
            Whether to return the sample likelihood.

        Returns
        -------
        int
            Sampled topic assignment.
        float
            Topic sample likelihood.
        """
        
        topic_probs = self.doc_counts[doc] + self.doc_prior
        topic_probs /= (self.doc_counts[doc] + self.doc_prior).sum()
        word_probs = self.topic_counts[:, word] + self.topic_prior
        word_probs /= (self.topic_counts + self.topic_prior).sum(-1)
        probs = topic_probs*word_probs
        probs /= probs.sum()
        topic = np.random.choice(self.n_topics, p=probs)

        if return_likelihood:
            return topic, probs[topic]
        return topic
    
    def sample(self, loc, word, doc, topic, return_likelihood=False):
        """Samples new document and topic assignments for a sample based on its
        word, document, and topic assignments.

        Parameters
        ----------
        loc : ndarray of shape=(3,)
            Sample location.
            Formatted as (image, x-coordinate, y-coordinate)
        word : int
            Word assignment.
        doc : int
            Document assignment.
        topic : int
            Topic assignment.
        return_likelihood : bool, default=False
            Whether to return the total sample likelihood.

        Returns
        -------
        int
            Sampled document assignment.
        int
            Sampled topic assignment.
        float
            Total sample likelihood.
        """
        
        doc_sample = self.sample_doc(loc, topic, return_likelihood)
        topic_sample = self.sample_topic(word, doc, return_likelihood)

        if return_likelihood:
            likelihood = doc_sample[1] + topic_sample[1]

            return doc_sample[0], topic_sample[0], likelihood
        return doc_sample, topic_sample

    def update(self, sample, step):
        """Updates a sample's document and topic assignments based on the
        previous step and return the total sample likelihood.

        Parameters
        ----------
        sample : int
            Sample index.
        step : int
            Step index.

        Returns
        -------
        float
            Total sample likelihood.
        """
        
        loc, (word, doc, topic) = self.corpus[sample, :3], self.corpus[sample, 3:].astype(np.int32)
        self.decrement(word, doc, topic)
        doc, topic, likelihood = self.sample(loc, word, doc, topic, return_likelihood=True)
        self.increment(word, doc, topic)
        self.corpus[sample, -2], self.corpus[sample, -1] = doc, topic
        self.topics[sample, step] = topic

        return likelihood
    
    def step(self, step):
        """Performs an update step for each sample of the dataset and returns
        the total step likelihood.

        Parameters
        ----------
        step : int
            Step index.

        Returns
        -------
        float
            Total step likelihood.
        """
        
        n_samples = self.corpus.shape[0]
        likelihood = 0

        for i in range(n_samples):
            likelihood += self.update(i, step)

        return likelihood

    def fit(self, X, n_steps=150, burn_in=50, desc='SLDA', verbosity=1):
        """Uses Gibbs sampling to infer document and topic membership for each 
        data sample based on its spatial location and data featurization.
        
        Parameters
        ----------
        X : ndarray of shape=(n_samples, n_features)
            Sample dataset.
        n_steps : int, default=150
            Total number of inference steps.
        burn_in : int, default=50
            Number of steps to discard.
        desc : str, default='SLDA'
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
        
        self.build(X, n_steps, burn_in)

        for i in tqdm(range(n_steps), desc) if verbosity == 1 else range(n_steps):
            step = (i - burn_in)%(n_steps - burn_in)
            self.likelihood_log.append(self.step(step))

        return self
    
    def transform(self, _=None):
        """Returns topic membership for each data sample as the mode of its
        recorded topic assignment history.
        
        Parameters
        ----------
        None

        Returns
        -------
        ndarray of shape=(n_samples,)
            Topic label for each data sample.
        """
        
        labels, _ = stats.mode(self.topics, -1)

        return labels

class sceLDA(BaseEstimator, TransformerMixin):
    """Implementation of single-cell embedded latent Dirichlet allocation.
    
    Parameters
    ----------
    n_topics : int, default=5
        Number of possible topics.
    n_docs : int, default=150
        Number of possible documents.
    n_words : int, default=15
        Number of possible words.
    n_neighbors : int, default=15
        Number of document neighbors
    doc_scale : float, default=1.0
        Size of document neighborhood.
    doc_prior : float, default=0.1
        Document distribution prior.
    topic_prior : float, default=0.1
        Topic distribution prior.
    layers : tuple | list of shape=(n_layers,)
        Encoder network dimensionality.
    seed : int, default=None
        Random state seed.

    Attributes
    ----------
    vae : VAE
        Variational autoencoder.
    slda : SLDA
        Spatial latent Dirichlet allocation.

    Usage
    -----
    >>> model = sceLDA(**kwargs)
    >>> topics = model.fit_transform(data, **kwargs)
    """

    def __init__(self, n_topics=5, n_docs=250, n_words=15, n_neighbors=15, doc_scale=1., doc_prior=.1, topic_prior=.1, layers=(100, 10), seed=None):
        super().__init__()
        set_seed(seed)

        self.n_topics = n_topics
        self.n_docs = n_docs
        self.n_words = n_words
        self.n_neighbors = n_neighbors
        self.doc_scale = doc_scale
        self.doc_prior = doc_prior
        self.topic_prior = topic_prior
        self.layers = layers
        self.seed = seed

        self.vae = VAE(layers, seed=None)
        self.slda = SLDA(n_topics, n_docs, n_words, n_neighbors, doc_scale, doc_prior, topic_prior, seed=None)

    def __eq__(self, other):
        return self.layers == other.layers and type(self.vae) is type(other.vae) and self.slda == other.slda

    def save(self, name='scelda'):
        """Creates a pickled sceLDA object and saves it to file.
        
        Parameters
        ----------
        name : str, default='scelda'
            Pickle file name

        Returns
        -------
        None
        """

        if name[-4:] != '.pkl':
            name += '.pkl'
        
        with open(name, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def fit(self, X, n_vae_steps=150, n_slda_steps=150, burn_in=50, learning_rate=1e-2, batch_size=None, test_size=.2, test_rate=1, vae_desc='VAE', slda_desc='SLDA', verbosity=1):
        """Performs dimensionality reduction using a variational autoencoder
        then infers anatomical labels for each encoded data sample using 
        spatial latent Dirichlet allocation.

        Parameters
        ----------
        X : ndarray of shape=(n_samples, n_features)
            Sample dataset.
        n_vae_steps : int, default=150
            Number of VAE training steps.
        n_slda_steps : int, default=150
            Total number of SLDA inference steps.
        burn_in : int, default=50
            Number of SLDA steps to discard.
        learning_rate : float, default=0.001
            VAE training step size.
        batch_size : int, default=None
            VAE training batch size.
        test_size : float, default=0.2
            VAE test dataset proportion.
        test_rate : int, default=1
            Number of steps between VAE validation tests.
        vae_desc : str, default='VAE'
            VAE model description
        slda_desc : str, default='SLDA'
            SLDA model description.
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

        locs, features = X[:, :3], torch.tensor(X[:, 3:], dtype=torch.float32)
        self.vae.fit(features, n_vae_steps, learning_rate, batch_size, test_size, test_rate, vae_desc, verbosity)
        Z = np.hstack([locs, self.vae.transform(features)])
        self.slda.fit(Z, n_slda_steps, burn_in, slda_desc, verbosity)

        return self
    
    def transform(self, X=None):
        """Returns the anatomical label for each data sample as its topic 
        membership obtained by spatial latent Dirichlet allocation.
        
        Parameters
        ----------
        X : Tensor of shape=(n_samples, n_features)
            Sample dataset.

        Returns
        -------
        ndarray of shape=(n_samples,)
            Anatomical label for each data sample.
        """

        labels = self.slda.transform(X)

        return labels
