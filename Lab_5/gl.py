from vec import Vec3
import numpy as np
from camera import Camera
from shading import phong_shade

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        # Ajusta la posición de la cámara y el FOV
        self.camera = Camera(center=Vec3(0, 0, -5), eye=Vec3(0, 0, 0), fov_deg=60, aspect=self.width/self.height)
        self.scene = []
        self.lights = []
        self.ambient = 0.2  # Puedes subir el ambiente para más luz

    def glRender(self):
        for y in range(self.height):
            v = 2.0 * (1.0 - (y + 0.5)/self.height) - 1.0
            for x in range(self.width):
                u = 2.0 * ((x + 0.5)/self.width) - 1.0
                O, D = self.camera.primary_ray(u, v)
                nearest_t = float('inf')
                hit_data = None
                for obj in self.scene:
                    hit = obj.ray_intersect(O, D)
                    if hit and hit[0] < nearest_t:
                        nearest_t = hit[0]
                        hit_data = hit
                if hit_data:
                    _, P, N, mat = hit_data
                    view_dir = -D
                    color = phong_shade(P, N, view_dir, mat, self.lights, self.ambient)
                    color = (color * 255).astype(int)
                    self.screen.set_at((x, y), (color[0], color[1], color[2]))
                else:
                    self.screen.set_at((x, y), (10, 10, 20))
        import pygame
        pygame.display.flip()