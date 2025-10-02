import os
import pygame
from pygame.locals import *
import numpy as np

from BMP.BMP_Writer import save as save_bmp
from Textures.gl import Raytracer
from Textures.MathLib import normalize
from Textures.material import Material, MAT_DIFFUSE, MAT_REFLECTIVE
from Textures.lights import AmbientLight, DirectionalLight, PointLight
from Textures.figures import Plane, Cube, Cylinder, Torus

# Resolución 
FAST_PREVIEW = True
WIDTH, HEIGHT = (800, 600) if FAST_PREVIEW else (512, 512)
WINDOW_TITLE  = "Lab 08"
OUTPUT_PATH   = os.path.join("renders", "Lab08_room_plus_centered.bmp")

#  Cámara 
CAMERA_POS = np.array([0.0, 1.2, 4.0], dtype=np.float32) 
FOV_DEG    = 70.0  

def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

SOFT_PINK = hexc('#f2cfc9')
MINT      = hexc('#b8caa5')
SKY       = hexc('#b4d8d4')
CORAL     = hexc('#dd785b')
OLIVE     = hexc('#c4c66a')
METAL     = (0.92, 0.92, 0.95)

def make_checker_floor_to_wall(rt,
                               y_plane=-1.0,
                               z_back=-8.0, z_front=3.5,
                               nx=12, nz=18,
                               tile_x=0.9, tile_z=0.9,
                               colA=(0.80,0.77,0.70),
                               colB=(0.64,0.61,0.55),
                               ks=0.25, shiny=85,
                               expand_eps=0.003):
    """
    Construye casillas como cubos delgados desde la pared del fondo (z_back)
    hasta debajo de la cámara (z_front), centrado en X.
    """
    total_x = nx * tile_x
    halfx   = total_x * 0.5

    slab_h  = 0.02
    y0 = y_plane - 1e-4
    y1 = y0 + slab_h

    bot_z = min(z_back, z_front)
    top_z = max(z_back, z_front)
    step_z = (top_z - bot_z) / nz

    for ix in range(nx):
        for iz in range(nz):
            x0 = -halfx + ix * tile_x
            x1 = x0 + tile_x
            z0 = bot_z + iz * step_z
            z1 = z0 + step_z

            x0 -= expand_eps; x1 += expand_eps
            z0 -= expand_eps; z1 += expand_eps

            color = colA if (ix + iz) % 2 == 0 else colB
            mat = Material(color=color, kd=0.78, ks=ks, shininess=shiny, mtype=MAT_REFLECTIVE)

            rt.scene.append(Cube(min_point=(x0, y0, z0), max_point=(x1, y1, z1), material=mat))

def build_room_and_floor(rt):
    wall    = Material(color=(0.96, 0.96, 0.97), kd=0.95, ks=0.05, shininess=14, mtype=MAT_DIFFUSE)
    ceiling = Material(color=(0.98, 0.98, 0.99), kd=0.96, ks=0.04, shininess=12, mtype=MAT_DIFFUSE)

    rt.scene = [
        Plane(position=(0.0, -1.0,  0.0), normal=(0,  1, 0),  material=wall),     # piso base del plano
        Plane(position=(0.0,  3.2,  0.0), normal=(0, -1, 0),  material=ceiling),  # techo
        Plane(position=(0.0,  0.0, -8.0), normal=(0,  0, 1),  material=wall),     # pared fondo
        Plane(position=(-4.8, 0.0,  0.0), normal=(1,  0, 0),  material=wall),     # pared izq
        Plane(position=( 4.8, 0.0,  0.0), normal=(-1, 0, 0),  material=wall),     # pared der
    ]

    make_checker_floor_to_wall(
        rt,
        y_plane=-1.0,
        z_back=-8.0, z_front=3.5,
        nx=14, nz=22,        # un poco más denso para esta proporción
        tile_x=0.9, tile_z=0.9,
        colA=(0.80,0.77,0.70), colB=(0.64,0.61,0.55),
        ks=0.25, shiny=85, expand_eps=0.003
    )

def add_objects(rt):
    matMetal = Material(color=METAL, kd=0.10, ks=0.90, shininess=200, mtype=MAT_REFLECTIVE)
    matMint  = Material(color=MINT,  kd=0.82, ks=0.18, shininess=45,  mtype=MAT_DIFFUSE)
    matSky   = Material(color=SKY,   kd=0.82, ks=0.18, shininess=45,  mtype=MAT_DIFFUSE)
    matPink  = Material(color=SOFT_PINK, kd=0.85, ks=0.15, shininess=40, mtype=MAT_DIFFUSE)
    matCoral = Material(color=CORAL, kd=0.83, ks=0.17, shininess=48,  mtype=MAT_DIFFUSE)
    matOlive = Material(color=OLIVE, kd=0.83, ks=0.17, shininess=48,  mtype=MAT_DIFFUSE)

    rt.scene += [
        Torus(position=(-2.5, 0.7, -7.2), R=1.15, r=0.38, material=matMetal),
        Torus(position=( 0.0, 0.7, -7.2), R=1.15, r=0.38, material=matMint),
        Torus(position=( 2.5, 0.7, -7.2), R=1.15, r=0.38, material=matPink),
    ]

    h_cyl = 1.40
    r_cyl = 0.55
    tile_top = -0.98
    cy = tile_top + h_cyl/2 + 0.01

    rt.scene += [
        Cylinder(position=(-2.5, cy, -4.2), radius=r_cyl, height=h_cyl, material=matCoral),
        Cylinder(position=( 0.0, cy, -4.2), radius=r_cyl, height=h_cyl, material=matSky),
        Cylinder(position=( 2.5, cy, -4.2), radius=r_cyl, height=h_cyl, material=matOlive),
    ]

# Luces
def setup_lights(rt):
    rt.lights = [
        AmbientLight(intensity=0.22),
        PointLight(position=(0.0, 3.0, -2.5), intensity=1.35),
        DirectionalLight(direction=normalize([ 0.4, -1.0, -0.2]), intensity=0.35),
        DirectionalLight(direction=normalize([-0.4, -1.0, -0.2]), intensity=0.35),
    ]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    rt = Raytracer(WIDTH, HEIGHT)
    rt.eye = CAMERA_POS
    rt.fov = FOV_DEG
    rt.backgroundColor = np.array([0.94, 0.95, 0.97], dtype=np.float32)

    build_room_and_floor(rt)
    add_objects(rt)
    setup_lights(rt)

    print("Renderizando…")
    try:
        rt.render()
    except AttributeError:
        rt.rtRender()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    save_bmp(OUTPUT_PATH, WIDTH, HEIGHT, rt.framebuffer)
    print(f" Guardado en {OUTPUT_PATH}")

    img = (np.clip(rt.framebuffer, 0, 1) * 255).astype(np.uint8)
    if img.shape[0] == HEIGHT and img.shape[1] == WIDTH:
        img = np.transpose(img, (1, 0, 2))
    surf = pygame.surfarray.make_surface(img)
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    print("ESC para salir")
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
