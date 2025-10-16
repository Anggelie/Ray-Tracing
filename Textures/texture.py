import numpy as np
import pygame

class ImageTexture:
    def __init__(self, path):
        surf = pygame.image.load(path)
        arr = pygame.surfarray.pixels3d(surf).astype(np.float32) / 255.0
        # pygame devuelve (W,H,3), convertimos a (H,W,3)
        self.img = np.transpose(arr, (1, 0, 2)).copy()
        self.h, self.w = self.img.shape[:2]

    def sample(self, u, v):
        # repeat
        u = u % 1.0
        v = v % 1.0
        x = u * (self.w - 1)
        y = (1.0 - v) * (self.h - 1)

        x0 = int(np.floor(x)); x1 = min(x0 + 1, self.w - 1)
        y0 = int(np.floor(y)); y1 = min(y0 + 1, self.h - 1)

        sx = x - x0; sy = y - y0

        c00 = self.img[y0, x0]
        c10 = self.img[y0, x1]
        c01 = self.img[y1, x0]
        c11 = self.img[y1, x1]

        c0 = c00 * (1 - sx) + c10 * sx
        c1 = c01 * (1 - sx) + c11 * sx
        c  = c0 * (1 - sy) + c1 * sy
        return c
