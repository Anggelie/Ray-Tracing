# material.py

class Material:
    def __init__(self, color, specular=0.5, shininess=32):
        """
        Material básico para el raytracer.

        :param color: tupla (r,g,b) con valores entre 0 y 1
        :param specular: coeficiente de especularidad (float)
        :param shininess: exponente para el brillo especular (int)
        """
        self.color = color
        self.specular = specular
        self.shininess = shininess
