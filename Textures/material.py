import numpy as np

MAT_DIFFUSE     = 0
MAT_REFLECTIVE  = 1
MAT_TRANSPARENT = 2  

class Material:
    def __init__(self, color=(1, 1, 1), kd=1.0, ks=0.0, shininess=32,
                 mtype=MAT_DIFFUSE, ior=1.0, **kwargs):
        self.color     = np.array(color, dtype=np.float32)
        self.kd        = float(kd)
        self.ks        = float(ks)
        self.shininess = float(shininess)
        self.mtype     = int(mtype)
        self.ior       = float(ior)
        self.texture   = kwargs.get("texture", None)
