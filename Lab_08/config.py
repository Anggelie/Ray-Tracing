import os

# Resolución 
# Para PRUEBAS rápidas:
WIDTH, HEIGHT = 256, 256

WINDOW_TITLE = "RayTracer Lab 08 – Pygame Viewer"

CAMERA_POSITION = (0.0, 1.0, 10.0)   # más lejos del cuarto
CAMERA_TARGET   = (0.0, 0.8, -9.0)   # mira hacia el centro del cuarto
CAMERA_UP       = (0.0, 1.0,  0.0)
FOV_DEG         = 40.0            

MAX_DEPTH = 2

AMBIENT_LIGHT        = (0.12, 0.12, 0.12)
ENV_INTENSITY        = 0.0
LIGHT_INTENSITY_SCALE = 1.0

def _repo_root():
    return os.path.dirname(os.path.abspath(__file__))

OUTPUT_PATH = os.path.join(_repo_root(), "renders", "Lab08_render_frontal.bmp")
