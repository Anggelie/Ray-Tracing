# Clase Vec3 para operaciones 3D

import numpy as np

class Vec3(np.ndarray):
    def __new__(cls, x, y, z):
        obj = np.asarray([x, y, z], dtype=float).view(cls)
        return obj

    @property
    def x(self): return self[0]
    @property
    def y(self): return self[1]
    @property
    def z(self): return self[2]

    def norm(self):
        return np.linalg.norm(self)

    def normalize(self):
        n = self.norm()
        return self if n == 0 else Vec3(*(self / n))

    def dot(self, other):
        return float(np.dot(self, other))

    def __sub__(self, other):
        return Vec3(*(super().__sub__(other)))

    def __add__(self, other):
        return Vec3(*(super().__add__(other)))

    def __mul__(self, other):
        return Vec3(*(super().__mul__(other)))

    def __rmul__(self, other):
        return Vec3(*(super().__mul__(other)))

    def clamp01(self):
        return Vec3(*(np.clip(self, 0, 1)))
