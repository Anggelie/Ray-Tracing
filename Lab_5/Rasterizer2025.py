# Rasterizer2025.py

import pygame
from pygame.locals import *
from gl import Renderer
from material import Material
from sphere import Sphere
from light import Light
from image_saver import ImageSaver

# -----------------------
# Configuración de ventana
# -----------------------
width  = 256
height = 256

pygame.init()
pygame.display.set_caption("Raytracer 2025")
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock  = pygame.time.Clock()

# -----------------------
# Renderer principal
# -----------------------
rend = Renderer(screen)

# -----------------------
# Construcción de la escena
# (mismo patrón de tus capturas):
#   rend.scene.append(Sphere(...))
# Incluyo try/except para que funcione si tu Sphere
# no acepta parámetros. Si no acepta, luego intento
# setear atributos si existen.
# -----------------------

def add_sphere_safe(pos, r, color=None):
    try:
        # Firma común: Sphere(position=(x,y,z), radius=..., color=(r,g,b))
        if color is not None:
            s = Sphere(position=pos, radius=r, color=color)
        else:
            s = Sphere(position=pos, radius=r)
        rend.scene.append(s)
        return
    except Exception:
        try:
            # Firma simple: Sphere()
            s = Sphere()
            # Si existen estos atributos, los seteamos:
            if hasattr(s, "position"): s.position = pos
            if hasattr(s, "radius"):   s.radius   = r
            if color is not None and hasattr(s, "color"):
                s.color = color
            rend.scene.append(s)
        except Exception:
            # Último recurso: agregar sin cambios
            rend.scene.append(Sphere())

# Materiales
red   = Material((1.0, 0.2, 0.2), specular=0.7, shininess=32)
green = Material((0.2, 1.0, 0.2), specular=0.5, shininess=16)
blue  = Material((0.2, 0.4, 1.0), specular=0.9, shininess=64)
gold  = Material((1.0, 0.84, 0.2), specular=1.0, shininess=128)

# Esferas
rend.scene.append(Sphere((0.0, 0.0, -5.0), 1.0, red))
rend.scene.append(Sphere((-1.6, -0.2, -4.0), 0.6, green))
rend.scene.append(Sphere((1.4, 0.3, -4.5), 0.8, blue))
rend.scene.append(Sphere((0.0, -1002.0, -5.0), 1000.0, gold))  # suelo

# Luz
rend.lights.append(Light(direction=(1, -1, -1), color=(1,1,1), intensity=1.2))

# -----------------------
# Render inicial
# -----------------------
rend.glRender()

# -----------------------
# Bucle principal (como tus capturas)
#   ESC o cerrar ventana -> salir
#   R -> re-render (útil si cambias escena)
#   S -> guardar BMP si tu GenerateBMP soporta Surface directamente
# -----------------------
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            isRunning = False
        if event.type == KEYDOWN and event.key == K_r:
            rend.glRender()
        if event.type == KEYDOWN and event.key == K_s:
            ImageSaver.save(screen, "raytracer.bmp")
    clock.tick(60)
pygame.quit()