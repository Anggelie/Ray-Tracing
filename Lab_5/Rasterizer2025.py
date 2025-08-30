from pygame.locals import *
from gl import Renderer
from material import Material
from sphere import Sphere
from light import Light
from image_saver import ImageSaver

width  = 512
height = 512

import pygame

pygame.init()
pygame.display.set_caption("Raytracer Lab 5 - 6 Esferas Metálicas")
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock  = pygame.time.Clock()

def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a RGB normalizado (0-1)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def create_six_spheres_scene(renderer):
    """Crea 6 esferas en formación 2x3 como perlas metálicas"""
    renderer.scene.clear()
    
    colors = [
        '#CBD183', 
        '#D17089',  
        '#6777B6', 
        '#92A2A6',
        '#8B9E15',
        '#D8560E' 
    ]
    
    materials = []
    for i, hex_color in enumerate(colors):
        rgb_color = hex_to_rgb(hex_color)
        material = Material(
            rgb_color, 
            specular=0.9, 
            shininess=128    
        )
        materials.append(material)
    
    positions = [
        (-2.5, 1.5, 0.0), 
        (0.0, 1.5, 0.0), 
        (2.5, 1.5, 0.0),  
        (-2.5, -1.5, 0.0), 
        (0.0, -1.5, 0.0),
        (2.5, -1.5, 0.0) 
    ]
    
    sphere_radius = 1.2
    for i in range(6):
        pos = positions[i]
        mat = materials[i]
        renderer.scene.append(Sphere(pos, sphere_radius, mat))

def setup_lights(renderer):
    """Configura iluminación para resaltar el efecto metálico"""
    renderer.lights.clear()
    
    # Luz principal fuerte desde arriba-derecha para crear highlights
    renderer.lights.append(Light(
        direction=(1, -0.5, -0.8), 
        color=(1.0, 1.0, 1.0), 
        intensity=1.5
    ))
    
    # Luz secundaria suave desde la izquierda
    renderer.lights.append(Light(
        direction=(-0.8, -0.3, -0.6), 
        color=(0.9, 0.95, 1.0), 
        intensity=0.4
    ))
    
    # Luz de relleno desde abajo para suavizar sombras
    renderer.lights.append(Light(
        direction=(0.2, 0.8, -0.2), 
        color=(1.0, 0.98, 0.95), 
        intensity=0.3
    ))

rend = Renderer(screen)

rend.camera.eye = (0, 0, 8) 
rend.camera.fov = 35  
rend.ambient = 0.05

setup_lights(rend)
create_six_spheres_scene(rend)

print("Iniciando renderizado de 6 esferas")
print("Presiona 'S' para guardar la imagen")
print("Presiona 'ESC' para salir")

# Renderizar la escena
rend.glRender()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            isRunning = False
        
        elif event.type == KEYDOWN and event.key == K_s:
            ImageSaver.save(screen, "ESFERAS.bmp")
            print("Imagen guardada como ESFERAS.bmp")
    
    clock.tick(60)

pygame.quit()
print("Renderizado completado!")