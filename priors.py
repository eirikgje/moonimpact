import numpy as np

class GaussianPrior(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def draw_samples(self, num_samples):
        return self.mean + self.std * np.random.randn(num_samples)

class UniformPrior(object):
    def __init__(self, minval, maxval):
        self.minval = minval
        self.maxval = maxval
        self.rrange = self.maxval - self.minval

    def draw_samples(self, num_samples):
        return self.minval + self.rrange * np.random.rand(num_samples)

class CertainPrior(object):
    def __init__(self, val):
        self.val = val

    def draw_samples(self, num_samples):
        return self.val
