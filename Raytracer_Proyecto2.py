import os
import pygame
from pygame.locals import *
import numpy as np

from BMP.BMP_Writer import save as save_bmp
from Textures.gl import Raytracer
from Textures.material import Material, MAT_DIFFUSE, MAT_REFLECTIVE
from Textures.lights import AmbientLight, DirectionalLight, PointLight
from Textures.figures import Plane, Cylinder, Torus, Ellipsoid, Sphere, Cube
from Textures.envmap import EnvMap
from Textures.texture import ImageTexture
from Textures.checker import CheckerTexture
from Textures.obj_loader import load_obj

def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

def tone_map(img: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    img = np.clip(img, 0.0, 1.0)
    return np.power(img, 1.0 / gamma)

WALL_LEFT = hexc('#D4A29A')
WALL_RIGHT = hexc('#9B5449')
BLUSH_PINK = hexc('#F5DCD6')
COOL_GREY = hexc('#6E7777')
DARK_GREY = hexc('#2E2F30')
COPPER_METAL = (0.75, 0.48, 0.35)

def build_final_scene(rt: Raytracer):
    rt.eye = np.array([0.0, 0.50, 6.5], dtype=np.float32)
    rt.fov = 38.0
    rt.max_depth = 4
    
    envmap_path = os.path.join("Textures", "env_sky.bmp")
    if os.path.exists(envmap_path):
        try:
            rt.envmap = EnvMap(envmap_path)
            rt.backgroundColor = np.array([0.7, 0.8, 0.95], dtype=np.float32)
        except:
            rt.envmap = None
            rt.backgroundColor = np.array([0.7, 0.8, 0.95], dtype=np.float32)
    else:
        rt.envmap = None
        rt.backgroundColor = np.array([0.7, 0.8, 0.95], dtype=np.float32)
    
    checker_tex = CheckerTexture(
        tiles_u=10, tiles_v=10,
        color_a=tuple(c*0.92 for c in WALL_LEFT),
        color_b=tuple(c*0.78 for c in WALL_LEFT)
    )
    floor_mat = Material(color=WALL_LEFT, kd=0.70, ks=0.30, shininess=100, texture=checker_tex)
    
    checker_grey = CheckerTexture(
        tiles_u=6, tiles_v=6,
        color_a=COOL_GREY,
        color_b=tuple(c*0.8 for c in COOL_GREY)
    )
    grey_mat = Material(color=COOL_GREY, kd=0.75, ks=0.25, shininess=90, texture=checker_grey)
    
    checker_wall = CheckerTexture(
        tiles_u=8, tiles_v=8,
        color_a=WALL_LEFT,
        color_b=tuple(c*0.9 for c in WALL_LEFT)
    )
    wall_mat = Material(color=WALL_LEFT, kd=0.85, ks=0.15, shininess=20, texture=checker_wall)
    
    checker_cylinder = CheckerTexture(
        tiles_u=4, tiles_v=2,
        color_a=DARK_GREY,
        color_b=tuple(min(1.0, c*1.3) for c in DARK_GREY)
    )
    dark_mat_textured = Material(color=DARK_GREY, kd=0.88, ks=0.12, shininess=30, texture=checker_cylinder)
    
    blush_mat = Material(color=BLUSH_PINK, kd=0.82, ks=0.18, shininess=70)
    dark_mat = Material(color=DARK_GREY, kd=0.88, ks=0.12, shininess=30)
    copper_mat = Material(color=COPPER_METAL, kd=0.05, ks=0.95, shininess=300, mtype=MAT_REFLECTIVE)
    tree_mat = Material(color=(0.3, 0.6, 0.3), kd=0.80, ks=0.20, shininess=60)
    
    rt.scene = [Plane(position=(0, -1.0, 0), normal=(0, 1, 0), material=floor_mat)]
    
    rt.scene.append(Torus(position=(0.0, -0.94, 0.0), R=1.10, r=0.09, material=blush_mat))
    rt.scene.append(Cylinder(position=(-0.05, -0.45, 0.0), radius=0.32, height=0.60, material=dark_mat))
    rt.scene.append(Cylinder(position=(0.28, -0.60, 0.0), radius=0.20, height=0.32, material=dark_mat_textured))
    rt.scene.append(Torus(position=(-0.05, 0.18, 0.0), R=0.90, r=0.24, material=blush_mat))
    rt.scene.append(Cylinder(position=(0.78, 0.18, -1.5), radius=0.50, height=3.5, material=wall_mat))
    rt.scene.append(Cylinder(position=(0.15, 0.08, 0.0), radius=0.78, height=0.15, material=grey_mat))
    rt.scene.append(Ellipsoid(position=(0.68, -0.52, 0.18), radii=(0.45, 0.45, 0.45), material=grey_mat))
    rt.scene.append(Ellipsoid(position=(-0.05, 1.08, 0.0), radii=(0.22, 0.22, 0.22), material=copper_mat))
    
    try:
        rt.scene.append(Cube(min_point=(-1.2, -0.98, -0.5), max_point=(-0.8, -0.6, -0.1), material=dark_mat))
    except:
        pass
    
    rt.scene.append(Sphere(position=(0.9, -0.85, -0.5), radius=0.15, material=copper_mat))
    rt.scene.append(Cylinder(position=(-1.5, -0.3, -1.0), radius=0.08, height=1.2, material=grey_mat))
    rt.scene.append(Sphere(position=(-1.5, 0.4, -1.0), radius=0.12, material=blush_mat))
    rt.scene.append(Sphere(position=(1.1, -0.80, 0.4), radius=0.18, material=blush_mat))
    
    obj_paths = [
        "Lowpoly_tree_sample.obj",
        os.path.join("models", "Lowpoly_tree_sample.obj"),
        os.path.join("assets", "models", "Lowpoly_tree_sample.obj"),
    ]
    
    for obj_path in obj_paths:
        if os.path.exists(obj_path):
            try:
                tree_triangles = load_obj(obj_path, material=tree_mat, scale=0.8, position=(2.5, -1.0, -1.5))
                rt.scene.extend(tree_triangles)
                break
            except:
                pass
    
    rt.lights = [
        AmbientLight(intensity=0.35),
        PointLight(position=(-1.5, 3.5, 3.5), intensity=1.8),
        DirectionalLight(direction=(0.7, -0.7, -0.3), intensity=0.30),
        DirectionalLight(direction=(-0.5, -0.6, 0.5), intensity=0.22),
    ]

def render_and_show(width, height, out_path, gamma=2.2):
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.SCALED)
    pygame.display.set_caption("Proyecto 2 - Ray Tracer")
    clock = pygame.time.Clock()

    rt = Raytracer(width, height)
    build_final_scene(rt)

    print(f"\n{'='*70}")
    print(f"  PROYECTO 2 - RAY TRACER")
    print(f"{'='*70}")
    print(f"  Resolucion: {width}x{height}")
    print(f"  Elementos: {len(rt.scene)}")
    print(f"  Luces: {len(rt.lights)}")
    print(f"  Max Depth: {rt.max_depth}")
    print(f"{'='*70}\n")

    try:
        rt.render()
    except AttributeError:
        rt.rtRender()

    fb = tone_map(rt.framebuffer, gamma=gamma)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    save_bmp(out_path, width, height, fb)
    
    print(f"\n{'='*70}")
    print(f"  RENDER COMPLETADO")
    print(f"  Archivo: {out_path}")
    print(f"{'='*70}\n")

    img = (np.clip(fb, 0, 1) * 255).astype(np.uint8)
    if img.shape[0] == height and img.shape[1] == width:
        img = np.transpose(img, (1, 0, 2))
    surf = pygame.surfarray.make_surface(img)
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False
        clock.tick(60)

    pygame.quit()

def main():
    print("\n" + "="*70)
    print("  PROYECTO 2 - RAY TRACER")
    print("="*70 + "\n")
    
    RES_PREVIEW = (480, 600)
    RES_FINAL = (960, 1200)

    OUTPUT_PREVIEW = os.path.join("renders", "proyecto2_preview.bmp")
    OUTPUT_FINAL = os.path.join("renders", "proyecto2_final.bmp")

    render_and_show(*RES_PREVIEW, OUTPUT_PREVIEW, gamma=2.1)

if __name__ == "__main__":
    main()