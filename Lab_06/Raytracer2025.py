import pygame
import os
import datetime

from gl import Renderer
from figures import Sphere
from material import Material, OPAQUE, REFLECTIVE, TRANSPARENT
from lights import DirectionalLight, AmbientLight

# -----------------------------------------------------------------
# Función para guardar el render en una carpeta con timestamp
# -----------------------------------------------------------------
def save_render(rend, folder="renders", prefix="Lab06"):
    """
    Guarda la superficie actual de Pygame en .bmp (24 bpp) con timestamp.
    - rend: tu Renderer (usa rend.screen como Surface destino).
    - folder: carpeta donde se guardarán las imágenes.
    - prefix: prefijo del nombre del archivo.
    """
    os.makedirs(folder, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"{prefix}_{ts}.bmp")
    pygame.image.save(rend.screen, path)
    print(f"[OK] Imagen guardada: {path}")
    return path

# -----------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------
def main():
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height), pygame.SCALED)
    pygame.display.set_caption("Lab 06 - Opaque, Reflective & Refractive Materials")
    clock = pygame.time.Clock()

    rend = Renderer(screen)
    rend.setEnvMap("Textures/bloem_field_sunrise_24.bmp")

    # --------------------------
    # Definición de materiales
    # --------------------------
    # OPAQUES
    yellowGreen = Material(diffuse=[200/255, 202/255, 102/255], spec=32, ks=0.4, matType=OPAQUE)
    violetGray  = Material(diffuse=[143/255, 113/255, 147/255], spec=32, ks=0.4, matType=OPAQUE)

    # REFLECTIVES
    mirror     = Material(diffuse=[1, 1, 1], spec=128, ks=0.5, matType=REFLECTIVE)
    chrome     = Material(diffuse=[0.9, 0.9, 0.9], spec=128, ks=0.5, matType=REFLECTIVE)

    # TRANSPARENTS
    glass      = Material(diffuse=[1, 1, 1], spec=64, ks=0.2, matType=TRANSPARENT, ior=1.5)
    water      = Material(diffuse=[0.9, 0.9, 1], spec=64, ks=0.2, matType=TRANSPARENT, ior=1.33)

    # --------------------------
    # Escena: 6 esferas
    # --------------------------
    rend.scene.append(Sphere(position=[-2.5, 1.5, -6], radius=1, material=yellowGreen)) # Opaque 1
    rend.scene.append(Sphere(position=[0,    1.5, -6], radius=1, material=violetGray))  # Opaque 2
    rend.scene.append(Sphere(position=[2.5,  1.5, -6], radius=1, material=mirror))      # Reflective 1
    rend.scene.append(Sphere(position=[-2.5,-1.0, -6], radius=1, material=chrome))      # Reflective 2
    rend.scene.append(Sphere(position=[0,   -1.0, -6], radius=1, material=glass))       # Transparent 1
    rend.scene.append(Sphere(position=[2.5, -1.0, -6], radius=1, material=water))       # Transparent 2

    # --------------------------
    # Luces
    # --------------------------
    rend.lights.append(AmbientLight(intensity=0.2))
    rend.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity=0.8))

    # --------------------------
    # Render principal
    # --------------------------
    rend.glRender()

    # Guardado automático al terminar el render
    save_render(rend)

    # --------------------------
    # Loop Pygame
    # --------------------------
    isRunning = True
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
                elif event.key == pygame.K_s:
                    save_render(rend)  # Guardar snapshot con S

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
