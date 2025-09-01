from vec import Vec3
from camera import Camera
from shading import phong_shade
import numpy as np

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        # Cámara más cerca y FOV más grande
        self.camera = Camera(center=Vec3(0, 0, -5), eye=Vec3(0, 0, -2), fov_deg=90, aspect=self.width/self.height)
        self.scene = []
        self.lights = []
        self.ambient = 0.4  # Más luz ambiente

    def glRender(self):
        for y in range(self.height):
            # Coordenadas normalizadas (0 a 1)
            v = y / self.height
            for x in range(self.width):
                u = x / self.width
                
                # Obtener rayo primario
                O, D = self.camera.primary_ray(u, v)
                
                # Buscar intersección más cercana
                nearest_t = float('inf')
                hit_data = None
                
                for obj in self.scene:
                    hit = obj.ray_intersect(O, D)
                    if hit and hit[0] < nearest_t and hit[0] > 0:  # Asegurar t > 0
                        nearest_t = hit[0]
                        hit_data = hit
                
                # Renderizar pixel
                if hit_data:
                    t, P, N, mat = hit_data
                    view_dir = -D.normalize()  # Dirección hacia la cámara
                    color = phong_shade(P, N, view_dir, mat, self.lights, self.ambient)
                    color = np.clip(color * 255, 0, 255).astype(int)
                    self.screen.set_at((x, y), tuple(color))
                else:
                    # Fondo negro
                    self.screen.set_at((x, y), (0, 0, 0))
        
        import pygame
        pygame.display.flip()