import struct

def GenerateBMP(filename, width, height, frameBuffer):
    row_padded = (width * 3 + 3) & ~3
    filesize = 54 + row_padded * height

    with open(filename, 'wb') as f:
        # Header BMP
        f.write(b'BM')
        f.write(struct.pack('<I', filesize))
        f.write(struct.pack('<HH', 0, 0))
        f.write(struct.pack('<I', 54))

        # DIB header
        f.write(struct.pack('<I', 40))   
        f.write(struct.pack('<I', width))
        f.write(struct.pack('<I', height))
        f.write(struct.pack('<H', 1))     
        f.write(struct.pack('<H', 24))   
        f.write(struct.pack('<I', 0))    
        f.write(struct.pack('<I', row_padded * height))
        f.write(struct.pack('<I', 2835))  
        f.write(struct.pack('<I', 2835))  
        f.write(struct.pack('<I', 0))    
        f.write(struct.pack('<I', 0))  

        for y in range(height-1, -1, -1):
            row_bytes = bytearray()
            for x in range(width):
                r, g, b = frameBuffer[y][x]
                r = max(0, min(255, int(r*255)))
                g = max(0, min(255, int(g*255)))
                b = max(0, min(255, int(b*255)))
                row_bytes += bytes([b, g, r])
            while len(row_bytes) < row_padded:
                row_bytes += b'\x00'
            f.write(row_bytes)
