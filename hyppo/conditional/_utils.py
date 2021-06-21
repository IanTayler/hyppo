import numpy as np

from ..tools import check_ndarray_xy, check_reps, contains_nan, convert_xy_float64


class _CheckInputs:
    """Checks inputs for all independence tests"""

    def __init__(self, x, y, z, reps=None):
        self.x = x
        self.y = y
        self.z = z
        self.reps = reps

    def __call__(self):
        check_ndarray_xy(self.x, self.y)
        check_ndarray_xy(self.y, self.z)
        contains_nan(self.x)
        contains_nan(self.y)
        self.x, self.y, self.z = self.check_dim_xy()
        self.x, self.y, self.z = convert_xy_float64(self.x, self.y, self.z)
        self._check_min_samples()
        self._check_variance()

        if self.reps:
            check_reps(self.reps)

        return self.x, self.y, self.z

    def check_dim_xyz(self):
        """Convert x, y and z to proper dimensions"""
        if self.x.ndim == 1:
            self.x = self.x[:, np.newaxis]
        elif self.x.ndim != 2:
            raise ValueError(
                "Expected a 2-D array `x`, found shape {}".format(self.x.shape)
            )
        if self.y.ndim == 1:
            self.y = self.y[:, np.newaxis]
        elif self.y.ndim != 2:
            raise ValueError(
                "Expected a 2-D array `y`, found shape {}".format(self.y.shape)
            )
        if self.z.ndim == 1:
            self.z = self.z[:, np.newaxis]
        elif self.z.ndim != 2:
            raise ValueError(
                "Expected a 2-D array `z`, found shape {}".format(self.z.shape)
            )

        self._check_nd_indeptest()

        return self.x, self.y

    def _check_nd_indeptest(self):
        """Check if number of samples is the same"""
        nx, _ = self.x.shape
        ny, _ = self.y.shape
        nz, _ = self.z.shape
        if nx != ny or ny != nz:
            raise ValueError(
                "Shape mismatch, x, y, and z must have shape [n, p], [n, q], [n, r]."
            )

    def _check_min_samples(self):
        """Check if the number of samples is at least 3"""
        nx = self.x.shape[0]
        ny = self.y.shape[0]
        nz = self.z.shape[0]

        if nx <= 3 or ny <= 3 or nz <= 3:
            raise ValueError("Number of samples is too low")

    def _check_variance(self):
        if np.var(self.x) == 0 or np.var(self.y) == 0 or np.var(self.z) == 0:
            raise ValueError("Test cannot be run, one of the inputs has 0 variance")
