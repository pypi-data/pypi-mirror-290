import numpy as np

from .normalization_base import Normalizer


class MinMaxScaler(Normalizer):
    def __init__(self, n_dim):
        self.min = np.array([np.inf] * n_dim)
        self.max = np.array([-np.inf] * n_dim)

    def update_min(self, x):
        self.min = np.fmin(self.min, x)

    def update_max(self, x):
        self.max = np.fmax(self.max, x)

    def partial_fit(self, x):
        self.update_min(x)
        self.update_max(x)

    def transform(self, x):
        denom = self.max - self.min
        if np.linalg.norm(denom) <= np.finfo(np.float64).eps:
            denom = 1
        return (x - self.min) / denom
