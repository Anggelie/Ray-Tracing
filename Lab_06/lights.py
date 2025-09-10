import numpy as np
from MathLib import reflectVector

def _normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

class AmbientLight(object):
    def __init__(self, color=[1, 1, 1], intensity=0.2):
        self.color = color
        self.intensity = float(intensity)

    def GetDiffuseColor(self, intercept, renderer):
        return [self.color[i] * self.intensity for i in range(3)]

    def GetSpecularColor(self, intercept, camera_pos, spec_power):
        return [0.0, 0.0, 0.0]


class DirectionalLight(object):
    """
    direction: vector que apunta DESDE la luz HACIA la escena
    """
    def __init__(self, direction=[-1, -1, -1], color=[1, 1, 1], intensity=1.0):
        self.direction = _normalize(np.array(direction, dtype=float))
        self.color = color
        self.intensity = float(intensity)

    def GetDiffuseColor(self, intercept, renderer):
        N = _normalize(np.array(intercept.normal, dtype=float))
        L = _normalize(-self.direction)
        ndotl = max(0.0, float(np.dot(N, L)))
        return [self.color[i] * self.intensity * ndotl for i in range(3)]

    def GetSpecularColor(self, intercept, camera_pos, spec_power):
        mat = intercept.obj.material
        ks = float(getattr(mat, "ks", 0.0))
        if ks <= 0.0:
            return [0.0, 0.0, 0.0]

        N = _normalize(np.array(intercept.normal, dtype=float))
        P = np.array(intercept.point, dtype=float)

        # L: del punto hacia la luz 
        L = _normalize(-self.direction)

        # Reflejo del vector incidente (-L) alrededor de N
        R = _normalize(reflectVector(N, -L))

        # V: del punto hacia la cámara
        V = _normalize(np.array(camera_pos, dtype=float) - P)

        rdotv = max(0.0, float(np.dot(R, V)))
        spec = (rdotv ** float(spec_power)) * ks

        return [self.color[i] * self.intensity * spec for i in range(3)]
