import pygame

class ImageSaver:
    @staticmethod
    def save(surface, filename="output.bmp"):
        pygame.image.save(surface, filename)
        print(f"Imagen guardada como {filename}")