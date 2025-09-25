import struct
import numpy as np

def save(filename, *args):
	"""Guarda un framebuffer en BMP 24bpp.

	Formas soportadas:
	- save(filename, framebuffer)  # framebuffer es numpy array (H,W,3) o lista de listas
	- save(filename, width, height, framebuffer)
	"""
	if len(args) == 1:
		frameBuffer = args[0]
		# intentar inferir width/height
		if isinstance(frameBuffer, np.ndarray):
			height, width = frameBuffer.shape[0], frameBuffer.shape[1]
		else:
			# lista de listas
			height = len(frameBuffer)
			width = len(frameBuffer[0]) if height > 0 else 0
	elif len(args) == 3:
		width, height, frameBuffer = args
	else:
		raise TypeError("save() acepta (filename, framebuffer) o (filename, width, height, framebuffer)")

	row_padded = (int(width) * 3 + 3) & ~3
	filesize = 54 + row_padded * int(height)

	with open(filename, 'wb') as f:
		# Header BMP
		f.write(b'BM')
		f.write(struct.pack('<I', filesize))
		f.write(struct.pack('<HH', 0, 0))
		f.write(struct.pack('<I', 54))

		# DIB header
		f.write(struct.pack('<I', 40))
		f.write(struct.pack('<I', int(width)))
		f.write(struct.pack('<I', int(height)))
		f.write(struct.pack('<H', 1))
		f.write(struct.pack('<H', 24))
		f.write(struct.pack('<I', 0))
		f.write(struct.pack('<I', row_padded * int(height)))
		f.write(struct.pack('<I', 2835))
		f.write(struct.pack('<I', 2835))
		f.write(struct.pack('<I', 0))
		f.write(struct.pack('<I', 0))

		for y in range(int(height)-1, -1, -1):
			row_bytes = bytearray()
			for x in range(int(width)):
				px = frameBuffer[y][x]
				# soportar numpy array o secuencia
				r = float(px[0]); g = float(px[1]); b = float(px[2])
				r = max(0, min(255, int(r*255)))
				g = max(0, min(255, int(g*255)))
				b = max(0, min(255, int(b*255)))
				row_bytes += bytes([b, g, r])
			while len(row_bytes) < row_padded:
				row_bytes += b'\x00'
			f.write(row_bytes)

