import numpy as np

class Intercept:
    """
    Resultado de una intersección rayo-objeto.
    - point:   punto de impacto (3,)
    - normal:  normal unitaria en el punto (3,)
    - distance: t del rayo (float)
    - obj:     referencia al objeto intersectado
    - texcoords: (u, v) opcional para texturas
    - rayDirection: dirección del rayo que pegó (3,) opcional
    """
    __slots__ = ("point", "normal", "distance", "obj", "texcoords", "rayDirection")

    def __init__(self, point, normal, distance, obj,
                 texcoords=None, rayDirection=None):
        self.point = np.asarray(point, dtype=np.float32)
        self.normal = np.asarray(normal, dtype=np.float32)
        self.distance = float(distance)
        self.obj = obj
        self.texcoords = texcoords
        self.rayDirection = (None if rayDirection is None
                             else np.asarray(rayDirection, dtype=np.float32))

    def __repr__(self):
        return (f"Intercept(point={self.point.tolist()}, "
                f"normal={self.normal.tolist()}, "
                f"distance={self.distance:.4f}, obj={type(self.obj).__name__})")
