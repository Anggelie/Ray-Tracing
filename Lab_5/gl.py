from vec import Vec3
import numpy as np
from camera import Camera
from shading import phong_shade

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        # Configuración de cámara más estándar
        self.camera = Camera(
            center=Vec3(0, 0, 0),    # Mirando hacia el origen
            eye=Vec3(0, 0, 8),       # Más lejos para mejor perspectiva
            fov_deg=45,              # FOV más conservador
            aspect=self.width/self.height
        )
        self.scene = []
        self.lights = []
        self.ambient = 0.1  # Luz ambiente más sutil

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