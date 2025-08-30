from vec import Vec3

class Camera:
    def __init__(self, center=Vec3(0,0,0), eye=Vec3(0,0,5), fov_deg=60, aspect=1):
        self.center = center
        self.eye = eye
        self.fov = fov_deg
        self.aspect = aspect

    def primary_ray(self, u, v):
        # Convertir FOV a radianes y calcular scale correctamente
        import math
        fov_rad = math.radians(self.fov)
        scale = math.tan(fov_rad * 0.5)
        
        # Coordenadas en screen space (-1 a 1)
        x = (2 * u - 1) * self.aspect * scale
        y = (2 * v - 1) * scale
        
        # Dirección del rayo (apuntando hacia -Z)
        direction = Vec3(x, y, -1).normalize()
        return self.eye, direction