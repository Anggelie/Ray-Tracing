# Lab 5: Spheres, Materials y Phong Shading
# Anggelie Velásquez
# 2025

from pygame.locals import *
from gl import Renderer
from material import Material
from sphere import Sphere
from light import DirectionalLight, AmbientLight
from image_saver import ImageSaver
import pygame

width  = 512
height = 512

pygame.init()
pygame.display.set_caption("Murciélago - Lab 5")
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

black     = Material((0.10, 0.10, 0.10), specular=0.50, shininess=64)
dark_gray = Material((0.30, 0.30, 0.30), specular=0.60, shininess=32)
cream     = Material((0.92, 0.88, 0.82), specular=0.35, shininess=24)
brown     = Material((0.45, 0.28, 0.12), specular=0.30, shininess=16)
green     = Material((0.45, 0.75, 0.25), specular=0.40, shininess=32)

# Cuerpo y cabeza
rend.scene.append(Sphere((0.0, 0.00, -5.0), 1.05, black))
rend.scene.append(Sphere((0.0, 0.95, -5.0), 0.70, black))

# Ojos
rend.scene.append(Sphere((-0.28, 1.07, -4.55), 0.22, cream))
rend.scene.append(Sphere(( 0.28, 1.07, -4.55), 0.22, cream))
rend.scene.append(Sphere((-0.28, 1.07, -4.35), 0.10, black))
rend.scene.append(Sphere(( 0.28, 1.07, -4.35), 0.10, black))

# Nariz
rend.scene.append(Sphere((0.00, 0.85, -4.35), 0.07, black))

# Orejas
rend.scene.append(Sphere((-0.46, 1.50, -5.00), 0.18, dark_gray))
rend.scene.append(Sphere(( 0.46, 1.50, -5.00), 0.18, dark_gray))

# Alas
rend.scene.append(Sphere((-1.20, 0.30, -5.20), 0.62, dark_gray))
rend.scene.append(Sphere(( 1.20, 0.30, -5.20), 0.62, dark_gray))
rend.scene.append(Sphere((-1.70,-0.32, -5.20), 0.42, dark_gray))
rend.scene.append(Sphere(( 1.70,-0.32, -5.20), 0.42, dark_gray))


branch_y  = -1.60
branch_z  = -5.30
count     = 20           # largo de la rama
spacing   = 0.22
radius    = 0.20         # grosor de la rama
start_x   = - (count - 1) * spacing * 0.5

for i in range(count):
    x = start_x + i * spacing
    rend.scene.append(Sphere((x, branch_y, branch_z), radius, brown))

rend.scene.append(Sphere((start_x + count * spacing, branch_y + 0.15, branch_z), 0.18, green))

branch_top = branch_y + radius
foot_r     = 0.15
toe_r      = 0.07
left_x, right_x = -0.35, 0.35
foot_y = branch_top + foot_r - 0.03
foot_z = -5.00

rend.scene.append(Sphere((left_x,  foot_y, foot_z),  foot_r, black))
rend.scene.append(Sphere((right_x, foot_y, foot_z),  foot_r, black))

toe_y = branch_top + toe_r - 0.02
toe_z = branch_z + 0.02  

# offsets laterales para los tres deditos
toe_dx = (-0.06, 0.0, 0.06)

for dx in toe_dx:
    rend.scene.append(Sphere((left_x  + dx, toe_y, toe_z),  toe_r, black))
    rend.scene.append(Sphere((right_x + dx, toe_y, toe_z), toe_r, black))

# Luces (key + fill + ambient) para solidez y volumen
rend.lights.append(DirectionalLight(direction=( 1, -1.2, -1),  color=(1,1,1), intensity=1.8))
rend.lights.append(DirectionalLight(direction=(-1, -0.2, -0.5), color=(1,1,1), intensity=0.6))
rend.lights.append(AmbientLight(color=(1,1,1), intensity=0.55))
rend.glRender()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                isRunning = False
            elif event.key == K_s:
                ImageSaver.save(screen, "bat.bmp")
    clock.tick(60)

pygame.quit()
