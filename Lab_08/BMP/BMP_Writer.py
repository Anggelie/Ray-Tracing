import struct

def save(filename, width, height, framebuffer):
    """
    Guarda un framebuffer en formato BMP (24 bits).
    - filename: ruta donde se guardará el archivo .bmp
    - width, height: dimensiones de la imagen
    - framebuffer: numpy array de shape (height, width, 3), valores [0,1]
    """

    with open(filename, "wb") as f:

        f.write(b'BM')  # signature
        filesize = 14 + 40 + (width * height * 3)
        f.write(struct.pack("<I", filesize))   
        f.write(struct.pack("<HH", 0, 0))     
        f.write(struct.pack("<I", 54))       

        # Info header (BITMAPINFOHEADER)
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

        #  Data 
        # BMP espera píxeles en orden BGR y de abajo hacia arriba
        for y in range(height):
            for x in range(width):
                r, g, b = framebuffer[height - 1 - y, x]  # invertimos filas
                r = int(max(0, min(1, r)) * 255)
                g = int(max(0, min(1, g)) * 255)
                b = int(max(0, min(1, b)) * 255)
                f.write(struct.pack("B", b))
                f.write(struct.pack("B", g))
                f.write(struct.pack("B", r))
