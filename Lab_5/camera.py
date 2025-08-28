from vec import Vec3

class Camera:
    def __init__(self, center=Vec3(0,0,0), eye=Vec3(0,0,5), fov_deg=60, aspect=1):
        self.center = center
        self.eye = eye
        self.fov = fov_deg
        self.aspect = aspect

    def primary_ray(self, u, v):
        fov_rad = self.fov * 3.14159 / 180
        x = u * self.aspect * (2 * (self.eye.z - self.center.z) * (3.14159 / 180) * self.fov / 2)
        y = v * (2 * (self.eye.z - self.center.z) * (3.14159 / 180) * self.fov / 2)
        direction = Vec3(x, y, -1).normalize()
        return self.eye, direction