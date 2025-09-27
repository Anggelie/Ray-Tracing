import numpy as np

class Intercept:
    """
    Contiene la información de una intersección rayo–objeto.

    Atributos:
    - point:     np.array([x,y,z]) punto de impacto en espacio mundo
    - normal:    np.array([x,y,z]) normal en el punto (puede venir normalizada)
    - distance:  float, parámetro t del rayo (distancia desde el origen)
    - obj:       referencia al objeto intersectado (para acceder a material, etc.)
    - texCoords: tupla/np.array opcional (u,v) si aplicas texturas
    - rayDirection: np.array dir del rayo que impactó (opcional)
    """
    __slots__ = ("point", "normal", "distance", "obj", "texCoords", "rayDirection")

    def __init__(self, point, normal, distance, obj=None, texCoords=None, rayDirection=None):
        self.point = np.array(point, dtype=np.float32)
        self.normal = np.array(normal, dtype=np.float32)
        self.distance = float(distance)
        self.obj = obj
        self.texCoords = texCoords
        self.rayDirection = (np.array(rayDirection, dtype=np.float32)
                             if rayDirection is not None else None)

    def __repr__(self):
        return (f"Intercept(point={self.point.tolist()}, "
                f"normal={self.normal.tolist()}, "
                f"distance={self.distance:.6f}, "
                f"obj={getattr(self.obj, 'type', type(self.obj).__name__)})")
