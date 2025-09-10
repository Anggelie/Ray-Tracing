import pygame
from math import atan2, acos, pi, tan, radians
from BMPTexture import BMPTexture
from MathLib import norm

class Camera:
    def __init__(self, translation=None, fov=60.0):
        self.translation = translation[:] if translation else [0.0, 0.0, 0.0]
        self.fov = float(fov)

class Renderer(object):
    def __init__(self, screen):
        # Pygame screen
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Escena y luces
        self.scene = []
        self.lights = []

        # Cámara
        self.camera = Camera([0.0, 0.0, 0.0], fov=60.0)

        # Parámetros globales
        self.clearColor = [0.0, 0.0, 0.0]
        self.currColor  = [1.0, 1.0, 1.0]
        self.maxRecursionDepth = 3

        # Environment map
        self.envMap = None

        # Pre-cálculos de proyección
        self.aspect = self.width / self.height
        self.tanHalfFov = tan(radians(self.camera.fov * 0.5))

    def glClearColor(self, r, g, b):
        self.clearColor = [r, g, b]

    def glColor(self, r, g, b):
        self.currColor = [r, g, b]

    def glClear(self):
        self.screen.fill([int(c * 255) for c in self.clearColor])

    def glPoint(self, x, y, color=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            c = color if color is not None else self.currColor
            r = max(0, min(255, int(c[0] * 255)))
            g = max(0, min(255, int(c[1] * 255)))
            b = max(0, min(255, int(c[2] * 255)))
            self.screen.set_at((x, y), (r, g, b))

    # Environment Map
    def setEnvMap(self, bmp_path):
        """Carga un BMP 24bpp para usar como environment map."""
        self.envMap = BMPTexture(bmp_path)

    def glEnvMap(self, orig, dir):
        """
        Mapeo equirectangular (lat-long):
          u = atan2(z, x)/(2π) + 0.5
          v = acos(-y)/π
        Invertimos V al samplear para corregir el fondo al revés.
        """
        if not self.envMap:
            return self.clearColor[:]

        d = norm(dir)
        u = (atan2(d[2], d[0]) / (2.0 * pi)) + 0.5
        v = acos(max(-1.0, min(1.0, -d[1]))) / pi

        return self.envMap.getColor(u, 1.0 - v)

    # Ray casting
    def glCastRay(self, orig, dir, ignore_obj=None, recursion=0):
        """
        Devuelve el Intercept más cercano o None.
        Cada objeto de la escena debe exponer .ray_intersect(orig, dir).
        """
        closest = None
        mindist = float("inf")

        for obj in self.scene:
            if obj is ignore_obj:
                continue
            hit = obj.ray_intersect(orig, dir)
            if hit and 0.0 < hit.distance < mindist:
                mindist = hit.distance
                closest = hit

        return closest

    # Render principal
    def _primary_ray_dir(self, px, py):
        """
        Genera la dirección del rayo primario para el pixel (px, py)
        usando un pinhole simple con FOV y aspecto.
        """
        # Normalized Device Coordinates en [-1, 1]
        x = (2.0 * (px + 0.5) / self.width  - 1.0) * self.aspect * self.tanHalfFov
        y = (1.0 - 2.0 * (py + 0.5) / self.height) * self.tanHalfFov
        z = -1.0
        return norm([x, y, z])

    def glRender(self):
        """
        Recorre cada pixel, lanza un rayo primario, sombrea con materiales
        y pinta en pantalla. Llama a pygame.display.flip() al final.
        """
        for y in range(self.height):
            for x in range(self.width):
                rayDir = self._primary_ray_dir(x, y)
                hit = self.glCastRay(self.camera.translation, rayDir)

                if hit is not None and hasattr(hit.obj, "material") and hit.obj.material:
                    color = hit.obj.material.GetSurfaceColor(hit, self, recursion=0)
                else:
                    color = self.glEnvMap(self.camera.translation, rayDir)

                self.glPoint(x, y, color)

        pygame.display.flip()
