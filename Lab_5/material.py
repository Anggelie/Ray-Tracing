# Material para Phong Shading

from vec import Vec3

class Material:
    def __init__(self, color, specular=0.5, shininess=32):
        self.color = color
        self.specular = specular
        self.shininess = shininess
