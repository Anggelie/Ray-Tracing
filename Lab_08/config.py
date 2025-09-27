import os

# Resolución (preview rápida)
WIDTH  = 480
HEIGHT = 360

WINDOW_TITLE = "RayTracer Lab 08 – Pygame Viewer"

# Cámara
CAMERA_POSITION = (2.2, 2.8, 5.0)
CAMERA_TARGET   = (0.0, 0.0, -1.0)
CAMERA_UP       = (0.0, 1.0,  0.0)
FOV_DEG         = 55.0

# Fondo
BG_COLOR = (0.12, 0.12, 0.13)

# Render progresivo (más alto = más rápido por frame)
PIXELS_PER_FRAME = 12000

# Recursión/Reflexiones (baja = más rápido)
MAX_DEPTH = 2

# Luces
AMBIENT_LIGHT        = (0.15, 0.15, 0.15)
ENV_INTENSITY        = 0.6
LIGHT_INTENSITY_SCALE = 1.0

# Salida BMP
import os
def _repo_root():
    return os.path.dirname(os.path.abspath(__file__))

OUTPUT_PATH = os.path.join(_repo_root(), "renders", "Lab08_render.bmp")
