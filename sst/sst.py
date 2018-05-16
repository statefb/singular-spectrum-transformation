# -*- coding: utf-8 -*-
import numpy as np
from numba import jit
from .util.linear_algebra import power_method

class SingularSpectrumTransformation():
    def __init__(self,win_length,n_components=3,order=None,lag=None,is_lanczos=True,rank_lanczos=None):
        """Change point detection with Singular Spectrum Transformation

        Parameters
        ----------
        win_length : int
        n_components : int
        order : int
        lag : int
        is_lanczos : boolean
        rank_lanczos : int

        """
        self.win_length = win_length
        self.n_components = n_components
        self.order = order
        self.lag = lag
        self.is_lanczos = is_lanczos
        self.rank_lanczos = rank_lanczos

    def score_offline(self,x):
        """calculate anomaly score (offline)

        Parameters
        ----------
        x : 1d numpy array

        Returns
        -------

        """
        if self.order is None:
            # rule of thumb
            self.order = self.win_length
        if self.lag is None:
            # rule of thumb
            self.lag = self.order // 2
        if self.rank_lanczos is None:
            # rule of thumb
            if self.n_components % 2 == 0:
                self.rank_lanczos = 2 * self.n_components
            else:
                self.rank_lanczos = 2 * self.n_components - 1

        # parameter validation
        assert isinstance(x,np.array), "input array must be numpy array."
        assert x.ndim == 1, "input array dimension must be 1."
        assert isinstance(self.win_length,int), "window length must be int."
        assert isinstance(self.n_components,int), "number of components must be int."
        assert isinstance(self.order,int), "order of partial time series must be int."
        assert isinstance(self.lag,int), "lag between test series and history series must be int."
        assert isinstance(self.rank_lanczos,int), "rank for lanczos must be int."



# @jit(nopython=True)
def sst_lanczos(X_test,X_history,rank,n_components):
    # calculate the first singular vec of test matrix
    u,_,_ = power_method(X_test,n_iter=2)
    C = X_history @ X_history.T
    T = lanczos(C,u,rank)
    val,vec = eig_tridiag(T)
    return 1 - (vec[0,:n_components] ** 2).sum()
