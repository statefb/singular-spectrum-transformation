# -*- coding: utf-8 -*-
from numba import jit
import numpy as np
from numpy.linalg import norm

# @jit(nopython=True)
def power_method(A,n_iter=2):
    """compute the first singular components by power method
    """
    m = A.shape[0]
    x0 = np.empty(m,dtype=np.float64)
    x0 = np.random.rand(m)
    x0 /= norm(x0)

    for i in range(n_iter):
        x0 = A.T @ A @ x0

    v = x0 / norm(x0)
    s = norm(A @ v)
    u = A @ v / s

    return u,s,v

@jit(nopython=True)
def lanczos(C,a,s):
    # initialization
    r = np.copy(a)
    a_pre = np.zeros_like(a,dtype=np.float64)
    beta_pre = 1
    T = np.zeros((s,s))

    for j in range(s):
        a_post = r / beta_pre
        alpha = a_post.T @ C @ a_post
        r = C @ a_post - alpha*a_post - beta_pre*a_pre
        beta_post = norm(r)

        T[j,j] = alpha
        if j - 1 >= 0:
            T[j,j-1] = beta_pre
            T[j-1,j] = beta_pre

        # update
        a_pre = a_post
        beta_pre = beta_post

    return T

@jit(nopython=True)
def eig_tridiag(T):
    # TODO: efficient implementation
    u,s,_ = np.linalg.svd(T)
    # return value must be ordered
    idcs = np.argsort(s)[::-1]
    return u[idcs],s[:,idcs]



"""
Python implementation (for debug)---------------------------------
"""

def power_method_py(A,n_iter=2):
    m = A.shape[0]
    x0 = np.empty(m,dtype=np.float64)
    x0 = np.random.rand(m)
    x0 /= norm(x0)

    for i in range(n_iter):
        x0 = A.T @ A @ x0

    v = x0 / norm(x0)
    s = norm(A @ v)
    u = A @ v / s

    return u,s,v

def lanczos_py(C,a,s):
    # initialization
    r = np.copy(a)
    a_pre = np.zeros_like(a,dtype=np.float64)
    beta_pre = 1
    T = np.zeros((s,s))

    for j in range(s):
        a_post = r / beta_pre
        alpha = a_post.T @ C @ a_post
        r = C @ a_post - alpha*a_post - beta_pre*a_pre
        beta_post = norm(r)

        T[j,j] = alpha
        if j - 1 >= 0:
            T[j,j-1] = beta_pre
            T[j-1,j] = beta_pre

        # update
        a_pre = a_post
        beta_pre = beta_post

    return T
