import os
import numpy as np

RENDER_PREVIEW = True
RENDER_FINAL   = True

# Resoluciones
RES_PREVIEW = (320, 400)          # rápido
RES_FINAL   = (960, 1200)         # entrega

# Salidas
def _out(name): return os.path.join("renders", name)
OUTPUT_PREVIEW = _out("p2_c_abstracto_preview.bmp")
OUTPUT_FINAL   = _out("p2_c_abstracto_final.bmp")

EYE = np.array([0.0, 1.2, 6.2], dtype=np.float32)
FOV = 38.0

USE_ENVMAP   = True
ENVMAP_PATH  = os.path.join("assets", "env_sky.jpg")

def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4))
SALMON_BG   = hexc('#c7796b')
SALMON_RING = hexc('#f2cfc9')
SLATE       = hexc('#5f6b6a')

WALL_COLOR   = SALMON_BG
FLOOR_COLOR  = SALMON_BG
RING_COLOR   = SALMON_RING
SLATE_COLOR  = SLATE
METAL_COLOR  = (0.92, 0.92, 0.94)

AMBIENT_INTENSITY = 0.20
POINT_LIGHTS = [ ((0.0, 3.1, -1.0), 1.2) ]
DIR_LIGHTS   = [ (( 0.6,-0.8, 0.2), 0.9), ((-0.7,-0.6,-0.3), 0.5) ]

COMPLEX_SCENE = True
