import numpy as np
from .MathLib import vec3

MAT_DIFFUSE    = 0
MAT_REFLECTIVE = 1

class Material(object):
    def __init__(self, color=(1,1,1), kd=1.0, ks=0.0, shininess=32.0, mtype=MAT_DIFFUSE):
        self.color = np.array(color, dtype=np.float32)
        self.kd = float(kd)           
        self.ks = float(ks)           
        self.shininess = float(shininess)
        self.mtype = mtype             
