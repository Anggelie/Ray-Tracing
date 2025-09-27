import numpy as np

class AmbientLight:
    def __init__(self, color=(1, 1, 1), intensity=0.1):
        """
        Luz ambiental: afecta toda la escena de manera uniforme.
        - color: tupla (r,g,b) entre 0 y 1
        - intensity: float, factor de intensidad
        """
        self.type = "Ambient"
        self.color = np.array(color, dtype=np.float32)
        self.intensity = float(intensity)


class DirectionalLight:
    def __init__(self, direction=(0, -1, 0), color=(1, 1, 1), intensity=1.0):
        """
        Luz direccional (como el sol).
        - direction: vector de dirección (se normaliza)
        - color: tupla (r,g,b) entre 0 y 1
        - intensity: float
        """
        self.type = "Directional"
        d = np.array(direction, dtype=np.float32)
        norm = np.linalg.norm(d)
        self.direction = d / norm if norm > 0 else d
        self.color = np.array(color, dtype=np.float32)
        self.intensity = float(intensity)


class PointLight:
    def __init__(self, position=(0, 0, 0), color=(1, 1, 1), intensity=1.0):
        """
        Luz puntual (bombilla).
        - position: coordenada (x,y,z)
        - color: tupla (r,g,b) entre 0 y 1
        - intensity: float
        """
        self.type = "Point"
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.intensity = float(intensity)
