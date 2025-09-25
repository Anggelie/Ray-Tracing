import numpy as np

EPS = 1e-6

def vec3(x, y=None, z=None):
    if y is None and z is None:
        v = np.array(x, dtype=np.float32)
        return v.astype(np.float32)
    return np.array([x, y, z], dtype=np.float32)

def length(v):
    return np.linalg.norm(v).astype(np.float32)

def normalize(v):
    n = np.linalg.norm(v)
    if n < EPS:
        return v.astype(np.float32)
    return (v / n).astype(np.float32)

def dot(a, b):
    return float(np.dot(a, b))

def cross(a, b):
    return np.cross(a, b).astype(np.float32)

def reflect(I, N):
    return (I - 2.0 * dot(I, N) * N).astype(np.float32)

def clamp01(x):
    return np.clip(x, 0.0, 1.0).astype(np.float32)

def faceforward(n, v):
    return n if dot(n, v) < 0.0 else -n
