# En esta parte pedi ayuda a ChatGPT para convertir una imagen BMP de 32 bits a 24 bits porque no me recordaba como hacerlo
from PIL import Image

# Abre tu archivo
img = Image.open("Textures/bloem_field_sunrise.bmp")

# Convierte a RGB (24 bits)
img = img.convert("RGB")

# Guarda otra vez en 24 bits
img.save("Textures/bloem_field_sunrise_24.bmp", "BMP")

print(" Imagen convertida a BMP 24 bits correctamente")
