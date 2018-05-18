# -*- coding: utf-8 -*-
"""unittest
"""
import unittest
import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal
from fastsst.sst import SingularSpectrumTransformation

class TestSingularSpectrumTransformation(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_sst(self):
        x = pd.read_csv("tests/test_data/freq_change.csv").values[:,0]
        sst = SingularSpectrumTransformation(win_length=70)
        score = sst.score_offline(x)
        assert score.size == x.size
        assert (score >= 0).all()

if __name__ == "__main__":
    unittest.main(verbosity=2)
