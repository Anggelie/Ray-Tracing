# Fuente de luz direccional

from vec import Vec3

class Light:
    def __init__(self, direction, color=Vec3(1,1,1), intensity=1.0):
        self.direction = Vec3(*direction).normalize()
        self.color = Vec3(*color)
        self.intensity = intensity
