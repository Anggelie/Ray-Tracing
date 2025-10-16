import numpy as np

class CheckerTexture:
    def __init__(self, tiles_u=8, tiles_v=8, color_a=(1,1,1), color_b=(0.1,0.1,0.1)):
        self.tu = max(1, int(tiles_u))
        self.tv = max(1, int(tiles_v))
        self.ca = np.array(color_a, dtype=np.float32)
        self.cb = np.array(color_b, dtype=np.float32)

    def sample(self, u: float, v: float):
        # wrap
        uu = u % 1.0
        vv = v % 1.0
        iu = int(uu * self.tu)
        iv = int(vv * self.tv)
        is_a = ((iu + iv) & 1) == 0
        return self.ca if is_a else self.cb
