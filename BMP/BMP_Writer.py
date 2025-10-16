import numpy as np
import struct

def save(filename, width, height, framebuffer):
    """
    Guarda una imagen BMP simple (24 bits sin compresión).
    framebuffer: numpy array (height, width, 3), valores en [0,1]
    """
    fb = np.clip(framebuffer, 0, 1)
    fb = (fb * 255).astype(np.uint8)

    with open(filename, "wb") as f:
        # Encabezado BMP
        filesize = 14 + 40 + width * height * 3
        f.write(b'BM')
        f.write(struct.pack("<I", filesize))
        f.write(b'\x00\x00')
        f.write(b'\x00\x00')
        f.write(struct.pack("<I", 14 + 40))

        f.write(struct.pack("<I", 40))
        f.write(struct.pack("<i", width))
        f.write(struct.pack("<i", height))
        f.write(struct.pack("<H", 1))
        f.write(struct.pack("<H", 24))
        f.write(struct.pack("<I", 0))
        f.write(struct.pack("<I", width * height * 3))
        f.write(struct.pack("<i", 0))
        f.write(struct.pack("<i", 0))
        f.write(struct.pack("<I", 0))
        f.write(struct.pack("<I", 0))

        # BMP se guarda de abajo hacia arriba
        for y in range(height):
            for x in range(width):
                r, g, b = fb[height - 1 - y, x]
                f.write(struct.pack('B', int(b)))
                f.write(struct.pack('B', int(g)))
                f.write(struct.pack('B', int(r)))
    print(f"Imagen guardada en {filename}")
