import math
from MathLib import sub, dot, norm
from intercept import Intercept

class Shape(object):
    def __init__(self, position=[0,0,0], material=None):
        self.position = position
        self.material = material

class Sphere(Shape):
    def __init__(self, position=[0,0,0], radius=1.0, material=None):
        super().__init__(position, material)
        self.radius = radius
        self.type = "sphere"

    def ray_intersect(self, orig, dir):
        L = sub(self.position, orig)
        tca = dot(L, dir)
        d2 = dot(L, L) - tca*tca
        r2 = self.radius*self.radius
        if d2 > r2:
            return None
        thc = math.sqrt(r2 - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0: t0 = t1
        if t0 < 0: return None

        p = [orig[0] + dir[0]*t0,
             orig[1] + dir[1]*t0,
             orig[2] + dir[2]*t0]

        normal = norm([p[0] - self.position[0],
                       p[1] - self.position[1],
                       p[2] - self.position[2]])

        # UV esféricas (equirectangular) basadas en la normal
        # u = atan2(nz, nx)/(2π) + 0.5
        # v = acos(-ny)/π
        u = (math.atan2(normal[2], normal[0]) / (2.0 * math.pi)) + 0.5
        v = math.acos(-normal[1]) / math.pi
        texCoords = (u, v)

        return Intercept(point=p, normal=normal, distance=t0,
                         texCoords=texCoords, rayDirection=dir, obj=self)
