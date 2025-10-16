import numpy as np
import pygame

class EnvMap:
    """
    Env map equirectangular (lat-long).
    Espera una imagen 8-bit RGB (png/jpg/bmp). Usa sample(direction)
    para obtener un color en [0,1].
    """
    def __init__(self, path: str):
        surf = pygame.image.load(path)        
        arr  = pygame.surfarray.pixels3d(surf).astype(np.float32) / 255.0
        self.img = np.transpose(arr, (1, 0, 2)).copy()
        self.h, self.w = self.img.shape[:2]

    def _bilinear(self, u: float, v: float):
        u = u % 1.0
        v = v % 1.0
        x = u * (self.w - 1)
        y = (1.0 - v) * (self.h - 1)

        x0 = int(np.floor(x)); x1 = min(x0 + 1, self.w - 1)
        y0 = int(np.floor(y)); y1 = min(y0 + 1, self.h - 1)

        sx = x - x0; sy = y - y0

        c00 = self.img[y0, x0]; c10 = self.img[y0, x1]
        c01 = self.img[y1, x0]; c11 = self.img[y1, x1]
        c0  = c00 * (1 - sx) + c10 * sx
        c1  = c01 * (1 - sx) + c11 * sx
        return c0 * (1 - sy) + c1 * sy

    def sample(self, direction):
        """
        direction: np.array([x,y,z]) normalizado.
        Mapeo equirectangular:
           u = atan2(z, x) / (2π) + 0.5
           v = acos(y) / π
        """
        d = direction / (np.linalg.norm(direction) + 1e-12)
        x, y, z = float(d[0]), float(d[1]), float(d[2])

        theta = np.arctan2(z, x)                  # [-pi, pi]
        phi   = np.arccos(np.clip(y, -1.0, 1.0))  # [0, pi]

        u = (theta / (2.0 * np.pi)) + 0.5         # [0,1]
        v =  phi / np.pi                          # [0,1]
        return self._bilinear(u, v)
