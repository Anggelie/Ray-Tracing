import struct

class BMPTexture(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            f.seek(10)
            pixel_data_offset = struct.unpack('<I', f.read(4))[0]
            f.seek(18)
            self.width  = struct.unpack('<I', f.read(4))[0]
            self.height = struct.unpack('<I', f.read(4))[0]
            f.seek(28)
            bpp = struct.unpack('<H', f.read(2))[0]
            if bpp != 24:
                raise Exception('BMPTexture: solo BMP 24bpp soportado')
            row_padded = (self.width * 3 + 3) & ~3

            self.pixels = []
            f.seek(pixel_data_offset)
            for _y in range(self.height):
                row = []
                row_bytes = f.read(row_padded)
                for x in range(self.width):
                    b = row_bytes[x*3 + 0]
                    g = row_bytes[x*3 + 1]
                    r = row_bytes[x*3 + 2]
                    row.append([r/255.0, g/255.0, b/255.0])
                self.pixels.insert(0, row)

    def getColor(self, u, v):
        u = u % 1.0
        v = v % 1.0
        x = int(u * (self.width  - 1))
        y = int(v * (self.height - 1))
        return self.pixels[y][x][:]
