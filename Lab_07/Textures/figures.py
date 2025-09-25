import numpy as np
from .MathLib import vec3, dot, cross, normalize, length, EPS
from .intercept import Intercept

class Shape(object):
    def __init__(self, material=None):
        self.material = material

    def ray_intersect(self, rayOrig, rayDir):
        return None

# PLANE
# Definido por un punto P0 y normal N 
# Ecuación: (P - P0) · N = 0
# t = ((P0 - O)·N) / (D·N)
class Plane(Shape):
    def __init__(self, position=(0,0,0), normal=(0,1,0), material=None):
        super().__init__(material)
        self.position = np.array(position, dtype=np.float32)
        self.normal = normalize(np.array(normal, dtype=np.float32))

    def ray_intersect(self, O, D):
        denom = dot(D, self.normal)
        if abs(denom) < EPS:
            return None
        t = dot(self.position - O, self.normal) / denom
        if t <= EPS:
            return None
        p = O + D * t
        n = self.normal
        return Intercept(point=p, normal=n, distance=float(t),
                         rayDirection=D, obj=self)

class Disk(Shape):
    def __init__(self, position=(0,0,0), normal=(0,1,0), radius=1.0, material=None):
        super().__init__(material)
        self.position = np.array(position, dtype=np.float32)
        self.normal = normalize(np.array(normal, dtype=np.float32))
        self.radius = float(radius)

    def ray_intersect(self, O, D):
        denom = dot(D, self.normal)
        if abs(denom) < EPS:
            return None
        t = dot(self.position - O, self.normal) / denom
        if t <= EPS:
            return None
        p = O + D * t
        v = p - self.position
        if dot(v, v) <= self.radius * self.radius:
            return Intercept(point=p, normal=self.normal, distance=float(t),
                             rayDirection=D, obj=self)
        return None

class Triangle(Shape):
    def __init__(self, A, B, C, material=None):
        super().__init__(material)
        self.A = np.array(A, dtype=np.float32)
        self.B = np.array(B, dtype=np.float32)
        self.C = np.array(C, dtype=np.float32)
        self._N = normalize(cross(self.B - self.A, self.C - self.A))

    def ray_intersect(self, O, D):
        e1 = self.B - self.A
        e2 = self.C - self.A
        pvec = np.cross(D, e2)
        det = dot(e1, pvec)
        if abs(det) < EPS:
            return None
        invDet = 1.0 / det
        tvec = O - self.A
        u = dot(tvec, pvec) * invDet
        if u < 0.0 or u > 1.0:
            return None
        qvec = np.cross(tvec, e1)
        v = dot(D, qvec) * invDet
        if v < 0.0 or (u + v) > 1.0:
            return None
        t = dot(e2, qvec) * invDet
        if t <= EPS:
            return None
        p = O + D * t
        n = self._N
        return Intercept(point=p, normal=n, distance=float(t),
                         rayDirection=D, obj=self)

class Cube(Shape):
    def __init__(self, min_corner, max_corner, material=None):
        super().__init__(material)
        self.min = np.array(min_corner, dtype=np.float32)
        self.max = np.array(max_corner, dtype=np.float32)

    def ray_intersect(self, O, D):
        invD = 1.0 / np.where(np.abs(D) < EPS, np.sign(D) * EPS, D)

        t1 = (self.min - O) * invD
        t2 = (self.max - O) * invD

        tmin = np.maximum.reduce(np.minimum(t1, t2))
        tmax = np.minimum.reduce(np.maximum(t1, t2))

        if tmax < max(tmin, EPS):
            return None

        t = tmin if tmin > EPS else tmax
        if t <= EPS:
            return None

        p = O + D * t
        n = np.zeros(3, dtype=np.float32)
        bias = 1e-3
        if abs(p[0] - self.min[0]) < bias: n = np.array([-1,0,0], dtype=np.float32)
        elif abs(p[0] - self.max[0]) < bias: n = np.array([ 1,0,0], dtype=np.float32)
        elif abs(p[1] - self.min[1]) < bias: n = np.array([0,-1,0], dtype=np.float32)
        elif abs(p[1] - self.max[1]) < bias: n = np.array([0, 1,0], dtype=np.float32)
        elif abs(p[2] - self.min[2]) < bias: n = np.array([0,0,-1], dtype=np.float32)
        else:                               n = np.array([0,0, 1], dtype=np.float32)

        return Intercept(point=p, normal=n, distance=float(t),
                         rayDirection=D, obj=self)
