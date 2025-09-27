import os
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_r

# Asegura imports relativos
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
if CURR_DIR not in sys.path:
    sys.path.append(CURR_DIR)

from config import (
    WIDTH, HEIGHT, WINDOW_TITLE, OUTPUT_PATH,
    CAMERA_POSITION, CAMERA_TARGET, CAMERA_UP, FOV_DEG,
    BG_COLOR
)

from BMP.BMP_Writer import save as save_bmp
from Textures.gl import Raytracer
from Textures.lights import AmbientLight, DirectionalLight, PointLight
from Textures.material import Material, MAT_DIFFUSE, MAT_REFLECTIVE, MAT_REFRACTIVE
from Textures.figures import Plane, Cylinder
from Textures.MathLib import normalize
import numpy as np


def build_scene(rt: Raytracer):
    """Aquí defines una escena mínima (3 cilindros) para el 50%."""
    # --- Materiales
    matte_green   = Material(color=(0.25, 0.65, 0.35), kd=0.9, ks=0.1, shininess=32,  mtype=MAT_DIFFUSE)
    metal_silver  = Material(color=(0.9, 0.9, 0.95),  kd=0.2, ks=0.7, shininess=120, mtype=MAT_REFLECTIVE, kr=0.7)
    glass_clear   = Material(color=(1.0, 1.0, 1.0),   kd=0.05, ks=0.1, shininess=64, mtype=MAT_REFRACTIVE, ior=1.5, kt=0.95, kr=0.05)

    wall_white = Material(color=(0.95, 0.95, 0.95), kd=0.9, ks=0.05, shininess=16, mtype=MAT_DIFFUSE)
    wall_warm  = Material(color=(0.90, 0.86, 0.80), kd=0.85, ks=0.05, shininess=16, mtype=MAT_DIFFUSE)
    floor_ref  = Material(color=(0.80, 0.78, 0.75), kd=0.5, ks=0.5, shininess=100, mtype=MAT_REFLECTIVE)

    # --- Cuarto + 3 cilindros
    rt.scene = [
        Plane(position=(0, -1.0,  0), normal=(0, 1, 0),  material=floor_ref),  # piso
        Plane(position=(0,  3.0,  0), normal=(0,-1, 0),  material=wall_warm),  # techo
        Plane(position=(0,  0,  -4), normal=(0, 0, 1),  material=wall_white),  # fondo
        Plane(position=(-3, 0,   0), normal=(1, 0, 0),  material=wall_warm),   # pared izq
        Plane(position=( 3, 0,   0), normal=(-1,0, 0),  material=wall_warm),   # pared der

        Cylinder(position=(-1.6, -0.2, -1.2), radius=0.45, height=1.6, material=matte_green),
        Cylinder(position=( 0.0, -0.5, -1.8), radius=0.35, height=2.2, material=metal_silver),
        Cylinder(position=( 1.4, -0.2, -0.6), radius=0.50, height=1.6, material=glass_clear),
    ]

    # --- Luces
    rt.lights = [
        AmbientLight(color=(1.0, 1.0, 1.0), intensity=0.12),
        DirectionalLight(direction=normalize([-0.6, -1.2, -0.5]), color=(1.0, 0.98, 0.95), intensity=0.9),
        DirectionalLight(direction=normalize([ 0.7, -0.6, -0.2]), color=(0.95, 0.97, 1.0), intensity=0.35),
        PointLight(position=(0.0, 2.8, -0.5), color=(1.0, 0.99, 0.97), intensity=0.6),
        PointLight(position=(0.0, 1.6, -3.0), color=(0.98, 0.96, 1.0), intensity=0.35),
    ]


def rt_to_surface(rt):
    """Convierte el framebuffer (float [0..1]) a una Surface de Pygame."""
    # array (H, W, 3) float -> uint8
    img = (np.clip(rt.framebuffer, 0, 1) * 255).astype(np.uint8)
    # Pygame espera (W, H) y bytes; creamos Surface y volcamos
    surface = pygame.Surface((rt.width, rt.height))
    pygame.surfarray.blit_array(surface, img.swapaxes(0, 1))  # swap para (W,H)
    return surface


def do_render(rt):
    """Renderiza con el Raytracer y retorna Surface."""
    print("Renderizando…")
    rt.render()
    print("Render listo.")
    return rt_to_surface(rt)


def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # --- Raytracer
    rt = Raytracer(
        WIDTH, HEIGHT,
        samples_per_pixel=4,
        enable_ao=True,
        ao_samples=8,
        ao_distance=2.0,
        max_depth=3
    )
    rt.backgroundColor = np.array(BG_COLOR, dtype=np.float32)

    # Cámara desde config
    rt.eye    = np.array(CAMERA_POSITION, dtype=np.float32)
    rt.target = np.array(CAMERA_TARGET,  dtype=np.float32)
    rt.up     = np.array(CAMERA_UP,      dtype=np.float32)
    rt.fov    = float(FOV_DEG)
    rt.update_camera()

    # Escena
    build_scene(rt)

    # Primer render
    surface = do_render(rt)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    isRunning = True
    while isRunning:
        for event in pygame.event.get():
            if event.type == QUIT:
                isRunning = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
                elif event.key == K_r:
                    # Re-render
                    surface = do_render(rt)
                    screen.blit(surface, (0, 0))
                    pygame.display.flip()

        clock.tick(60)

    # Guardar BMP al salir
    ensure_dir(OUTPUT_PATH)
    save_bmp(OUTPUT_PATH, rt.width, rt.height, rt.framebuffer)
    print(f"Imagen guardada en: {OUTPUT_PATH}")

    pygame.quit()


if __name__ == "__main__":
    main()
