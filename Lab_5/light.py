# light.py
import numpy as np

class Light:
    def __init__(self, color=(1,1,1), intensity=1.0, light_type="Base"):
        self.color = np.array(color, dtype=float)
        self.intensity = float(intensity)
        self.light_type = light_type

    def energy(self):
        # Color * intensidad
        return self.color * self.intensity


class AmbientLight(Light):
    def __init__(self, color=(1,1,1), intensity=0.1):
        super().__init__(color, intensity, "Ambient")


class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0), color=(1,1,1), intensity=1.0):
        super().__init__(color, intensity, "Directional")
        d = np.array(direction, dtype=float)
        n = np.linalg.norm(d)
        self.direction = d / (n if n > 0 else 1.0)  # normalizada


class PointLight(Light):
    def __init__(self, position=(0,0,0), color=(1,1,1), intensity=1.0,
                 att_constant=1.0, att_linear=0.09, att_quadratic=0.032):
        super().__init__(color, intensity, "Point")
        self.position = np.array(position, dtype=float)
        self.att_constant = float(att_constant)
        self.att_linear = float(att_linear)
        self.att_quadratic = float(att_quadratic)

    def attenuation(self, dist):
        # 1 / (k_c + k_l d + k_q d^2)
        den = self.att_constant + self.att_linear*dist + self.att_quadratic*(dist*dist)
        return 1.0 / max(den, 1e-6)
