from math import sqrt
from vec import Vec3

class Sphere:
    def __init__(self, position, radius, material):
        self.position = Vec3(*position)
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin, direction):
        L = self.position - origin
        tca = L.dot(direction)
        d2 = L.dot(L) - tca * tca
        r2 = self.radius * self.radius
        if d2 > r2:
            return None
        thc = (r2 - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        t = t0 if t0 > 0 else t1
        if t < 0:
            return None
        hit = origin + direction * t
        normal = (hit - self.position).normalize()
        return (t, hit, normal, self.material)
