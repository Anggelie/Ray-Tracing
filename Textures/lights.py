import numpy as np

def _to_vec3(v):
    return np.array(v, dtype=np.float32)

def _normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

class AmbientLight:
    """Luz ambiental uniforme."""
    def __init__(self, color=(1, 1, 1), intensity=0.2):
        self.type = "AMBIENT"
        self.color = _to_vec3(color)
        self.intensity = float(intensity)

class DirectionalLight:
    """Luz direccional (sol)."""
    def __init__(self, direction, color=(1, 1, 1), intensity=1.0):
        self.type = "DIRECTIONAL"
        self.direction = _normalize(_to_vec3(direction))  # hacia el objeto
        self.color = _to_vec3(color)
        self.intensity = float(intensity)

class PointLight:
    """Luz puntual con atenuación simple."""
    def __init__(self, position, color=(1, 1, 1), intensity=1.0):
        self.type = "POINT"
        self.position = _to_vec3(position)
        self.color = _to_vec3(color)
        self.intensity = float(intensity)
