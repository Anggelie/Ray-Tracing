import numpy as np

MAT_DIFFUSE     = 0
MAT_REFLECTIVE  = 1
MAT_REFRACTIVE  = 2


def _to_vec3(c):
    """Convierte tupla/lista a np.array float32 de 3 componentes."""
    v = np.array(c, dtype=np.float32)
    if v.shape != (3,):
        raise ValueError("color debe ser (r, g, b)")
    return v


class Material:
    """
    Material básico para el RayTracer.

    Parámetros:
    - color: (r,g,b) en [0,1].
    - kd: coeficiente difuso (0..1).
    - ks: coeficiente especular (0..1).
    - shininess: exponente Phong (p. ej. 16, 32, 64, 128).
    - mtype: MAT_DIFFUSE, MAT_REFLECTIVE, MAT_REFRACTIVE.
    - ior: índice de refracción (solo refractivos). Ej: 1.5 (vidrio).
    - kr: fuerza de reflexión [0..1] (solo reflectivos o mix).
    - kt: fuerza de transmisión [0..1] (solo refractivos o mix).

    Nota: puedes usar materiales “híbridos” (p. ej. un metal con algo
    de difusión y brillo) ajustando kd/ks/kr/kt a tu gusto.
    """
    def __init__(
        self,
        color=(1.0, 1.0, 1.0),
        kd=1.0,
        ks=0.0,
        shininess=32.0,
        mtype=MAT_DIFFUSE,
        ior=1.5,
        kr=0.5,
        kt=0.9,
    ):
        self.color     = _to_vec3(color)
        self.kd        = float(kd)
        self.ks        = float(ks)
        self.shininess = float(shininess)

        self.mtype = int(mtype)

        self.ior = float(ior) 
        self.kr  = float(kr)  
        self.kt  = float(kt)  

        self.kd = max(0.0, min(1.0, self.kd))
        self.ks = max(0.0, min(1.0, self.ks))
        self.kr = max(0.0, min(1.0, self.kr))
        self.kt = max(0.0, min(1.0, self.kt))

    def __repr__(self):
        return (f"Material(color={tuple(self.color)}, kd={self.kd}, ks={self.ks}, "
                f"shininess={self.shininess}, mtype={self.mtype}, "
                f"ior={self.ior}, kr={self.kr}, kt={self.kt})")


def matte(color=(0.8, 0.8, 0.8), kd=0.9):
    """Difuso mate sencillo."""
    return Material(color=color, kd=kd, ks=0.05, shininess=16, mtype=MAT_DIFFUSE)

def metal(color=(0.9, 0.9, 0.95), ks=0.7, shininess=120, kr=0.7):
    """Reflectivo tipo metal pulido (con algo de especular)."""
    return Material(color=color, kd=0.2, ks=ks, shininess=shininess,
                    mtype=MAT_REFLECTIVE, kr=kr)

def glass(color=(1.0, 1.0, 1.0), ior=1.5, kr=0.05, kt=0.95):
    """Refractante tipo vidrio transparente."""
    return Material(color=color, kd=0.05, ks=0.1, shininess=64,
                    mtype=MAT_REFRACTIVE, ior=ior, kr=kr, kt=kt)
