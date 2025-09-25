import numpy as np
from .MathLib import normalize, dot, reflect, clamp01

LT_AMBIENT     = 0
LT_DIRECTIONAL = 1
LT_POINT       = 2
LT_SPOT        = 3  

class Light(object):
    def __init__(self, color=(1,1,1), intensity=1.0):
        self.color = np.array(color, dtype=np.float32)
        self.intensity = float(intensity)
        self.lightType = LT_AMBIENT

    def GetLightColor(self, **_):
        return self.color * self.intensity

    def GetSpecularColor(self, **_):
        return np.array([0,0,0], dtype=np.float32)

class AmbientLight(Light):
    def __init__(self, color=(1,1,1), intensity=0.1):
        super().__init__(color, intensity)
        self.lightType = LT_AMBIENT

class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0), color=(1,1,1), intensity=1.0):
        super().__init__(color, intensity)
        self.direction = normalize(np.array(direction, dtype=np.float32))
        self.lightType = LT_DIRECTIONAL

    def _L(self, _inter):
        # L = dirección de la luz desde el punto
        return -self.direction

    def GetLightColor(self, inter=None, viewDir=None, **_):
        if inter is None: return np.array([0,0,0], dtype=np.float32)
        N = inter.normal
        L = self._L(inter)
        ndotl = max(0.0, dot(N, L))
        return self.color * self.intensity * ndotl

    def GetSpecularColor(self, inter=None, viewDir=None, **_):
        if inter is None or viewDir is None: return np.array([0,0,0], dtype=np.float32)
        N = inter.normal
        L = self._L(inter)
        ndotl = max(0.0, dot(N, L))
        if ndotl <= 0.0: return np.array([0,0,0], dtype=np.float32)
        R = reflect(-L, N)
        spec = max(0.0, dot(R, viewDir)) ** inter.obj.material.shininess
        return self.color * self.intensity * spec

class PointLight(Light):
    def __init__(self, position=(0,0,0), color=(1,1,1), intensity=1.0):
        super().__init__(color, intensity)
        self.position = np.array(position, dtype=np.float32)
        self.lightType = LT_POINT

    def _L(self, inter):
        return normalize(self.position - inter.point)

    def GetLightColor(self, inter=None, viewDir=None, **_):
        if inter is None: return np.array([0,0,0], dtype=np.float32)
        N = inter.normal
        L = self._L(inter)
        ndotl = max(0.0, dot(N, L))
        return self.color * self.intensity * ndotl

    def GetSpecularColor(self, inter=None, viewDir=None, **_):
        if inter is None or viewDir is None: return np.array([0,0,0], dtype=np.float32)
        N = inter.normal
        L = self._L(inter)
        ndotl = max(0.0, dot(N, L))
        if ndotl <= 0.0: return np.array([0,0,0], dtype=np.float32)
        R = reflect(-L, N)
        spec = max(0.0, dot(R, viewDir)) ** inter.obj.material.shininess
        return self.color * self.intensity * spec
