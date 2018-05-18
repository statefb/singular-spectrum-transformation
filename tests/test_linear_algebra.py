# -*- coding: utf-8 -*-
"""unittest
"""
import unittest
import numpy as np
from numpy.testing import assert_almost_equal
from fastsst.util.linear_algebra import *

class TestLinearAlgebra(unittest.TestCase):
    def setUp(self):
        np.random.seed(1234)
        self.A = np.random.rand(10,10)
        self.x0 = np.random.rand(10)
        self.x0 /= np.linalg.norm(self.x0)

        d = 3*np.ones(10)
        e = -1*np.ones(10 - 1)
        self.T = np.diag(d) + np.diag(e,k=1) + np.diag(e,k=-1)

    def tearDown(self):
        pass

    def test_power_method(self):
        u_pow,s_pow,_ = power_method(self.A,self.x0,n_iter=100)
        U_np,s_np,_ = np.linalg.svd(self.A)
        assert_almost_equal(s_pow,s_np[0])
        assert_almost_equal(np.abs(u_pow),np.abs(U_np[:,0]))

    def test_eig_tridiag(self):
        U_tri,s_tri = eig_tridiag(self.T)
        U_np,s_np,_ = np.linalg.svd(self.T)
        assert_almost_equal(s_tri,s_np)
        assert_almost_equal(np.abs(U_tri),np.abs(U_np))


if __name__ == "__main__":
    unittest.main(verbosity=2)
