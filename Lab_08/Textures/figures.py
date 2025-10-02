import numpy as np
from Textures.MathLib import normalize
from Textures.intercept import Intercept
from Textures.material import Material

EPS = 1e-6

#   Clase base
class Shape:
    def __init__(self, position, material: Material):
        self.position = np.array(position, dtype=np.float32) if position is not None else None
        self.material = material
        self.type = "Shape"

    def ray_intersect(self, orig, dir):
        raise NotImplementedError


#   Esfera
class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = float(radius)
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        L = self.position - orig
        tca = np.dot(L, dir)
        d2 = np.dot(L, L) - tca * tca
        r2 = self.radius * self.radius
        if d2 > r2:
            return None
        thc = np.sqrt(r2 - d2)
        t0 = tca - thc
        t1 = tca + thc

        t = t0 if t0 > EPS else t1
        if t < EPS:
            return None

        hit = orig + dir * t
        normal = normalize(hit - self.position)
        return Intercept(point=hit, normal=normal, distance=t, obj=self)


#   Plano infinito
class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normalize(np.array(normal, dtype=np.float32))
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        if abs(denom) < 1e-6:
            return None  # rayo paralelo
        t = np.dot(self.position - orig, self.normal) / denom
        if t < EPS:
            return None
        hit = orig + dir * t
        return Intercept(point=hit, normal=self.normal, distance=t, obj=self)


#   Disco
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = float(radius)
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        plane_hit = super().ray_intersect(orig, dir)
        if plane_hit is None:
            return None
        v = plane_hit.point - self.position
        if np.dot(v, v) <= self.radius * self.radius + 1e-8:
            return plane_hit
        return None


#   Triángulo
class Triangle(Shape):
    def __init__(self, A, B, C, material):
        super().__init__(A, material)  # usamos A como punto del plano
        self.A = np.array(A, dtype=np.float32)
        self.B = np.array(B, dtype=np.float32)
        self.C = np.array(C, dtype=np.float32)
        self.normal = normalize(np.cross(self.B - self.A, self.C - self.A))
        self.type = "Triangle"

    def ray_intersect(self, orig, dir):
        # Intersección con el plano del triángulo
        denom = np.dot(dir, self.normal)
        if abs(denom) < 1e-6:
            return None
        t = np.dot(self.A - orig, self.normal) / denom
        if t < EPS:
            return None

        P = orig + dir * t

        # Prueba baricéntrica
        v0 = self.C - self.A
        v1 = self.B - self.A
        v2 = P - self.A

        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        invDen = 1.0 / (dot00 * dot11 - dot01 * dot01 + 1e-20)
        u = (dot11 * dot02 - dot01 * dot12) * invDen
        v = (dot00 * dot12 - dot01 * dot02) * invDen

        if (u >= -1e-6) and (v >= -1e-6) and (u + v <= 1.0 + 1e-6):
            return Intercept(point=P, normal=self.normal, distance=t, obj=self)

        return None

class Cube(Shape):
    def __init__(self, min_point, max_point, material):
        super().__init__(min_point, material)
        self.min = np.array(min_point, dtype=np.float32)
        self.max = np.array(max_point, dtype=np.float32)
        self.type = "Cube"

    def ray_intersect(self, orig, dir):
        inv = 1.0 / (dir + 1e-12)
        tmin = (self.min - orig) * inv
        tmax = (self.max - orig) * inv

        t1 = np.minimum(tmin, tmax)
        t2 = np.maximum(tmin, tmax)

        t_near = np.max(t1)
        t_far = np.min(t2)

        if t_near > t_far or t_far < 0:
            return None

        t = t_near if t_near > EPS else t_far
        if t < EPS:
            return None

        hit = orig + dir * t

        # Normal de la cara tocada
        eps = 1e-4
        normal = np.zeros(3, dtype=np.float32)
        if abs(hit[0] - self.min[0]) < eps: normal = np.array([-1, 0, 0], dtype=np.float32)
        elif abs(hit[0] - self.max[0]) < eps: normal = np.array([ 1, 0, 0], dtype=np.float32)
        elif abs(hit[1] - self.min[1]) < eps: normal = np.array([ 0,-1, 0], dtype=np.float32)
        elif abs(hit[1] - self.max[1]) < eps: normal = np.array([ 0, 1, 0], dtype=np.float32)
        elif abs(hit[2] - self.min[2]) < eps: normal = np.array([ 0, 0,-1], dtype=np.float32)
        elif abs(hit[2] - self.max[2]) < eps: normal = np.array([ 0, 0, 1], dtype=np.float32)

        return Intercept(point=hit, normal=normal, distance=t, obj=self)


#   Cilindro (eje Y) con tapas
class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = float(radius)
        self.height = float(height)
        self.type = "Cylinder"

    def ray_intersect(self, orig, dir):
        cx, cy, cz = self.position
        ox, oy, oz = orig
        dx, dy, dz = dir

        ox -= cx; oy -= cy; oz -= cz

        a = dx*dx + dz*dz
        b = 2.0 * (ox*dx + oz*dz)
        c = ox*ox + oz*oz - self.radius*self.radius

        t_side = None
        n_side = None

        if abs(a) > 1e-12:
            disc = b*b - 4*a*c
            if disc >= 0.0:
                rdisc = np.sqrt(disc)
                t0 = (-b - rdisc) / (2*a)
                t1 = (-b + rdisc) / (2*a)
                if t0 > t1: t0, t1 = t1, t0

                for t_candidate in (t0, t1):
                    if t_candidate > EPS:
                        y_hit = oy + dy * t_candidate
                        y_min = -self.height * 0.5
                        y_max =  self.height * 0.5
                        if y_min - 1e-6 <= y_hit <= y_max + 1e-6:
                            t_side = t_candidate
                            hit_local = np.array([ox + dx*t_side, y_hit, oz + dz*t_side], dtype=np.float32)
                            n_local = np.array([hit_local[0], 0.0, hit_local[2]], dtype=np.float32)
                            n_side = normalize(n_local)
                            break

        t_cap = None
        n_cap = None
        y_min = -self.height * 0.5
        y_max =  self.height * 0.5

        if abs(dy) > 1e-12:
            t_top = (y_max - oy) / dy
            if t_top > EPS:
                xh = ox + dx * t_top
                zh = oz + dz * t_top
                if (xh*xh + zh*zh) <= self.radius*self.radius + 1e-8:
                    t_cap = t_top
                    n_cap = np.array([0.0, 1.0, 0.0], dtype=np.float32)

            t_bottom = (y_min - oy) / dy
            if t_bottom > EPS:
                xh = ox + dx * t_bottom
                zh = oz + dz * t_bottom
                if (xh*xh + zh*zh) <= self.radius*self.radius + 1e-8:
                    if t_cap is None or t_bottom < t_cap:
                        t_cap = t_bottom
                        n_cap = np.array([0.0, -1.0, 0.0], dtype=np.float32)

        t = None
        n_local = None
        if t_side is not None and t_cap is not None:
            if t_side < t_cap:
                t, n_local = t_side, n_side
            else:
                t, n_local = t_cap, n_cap
        elif t_side is not None:
            t, n_local = t_side, n_side
        elif t_cap is not None:
            t, n_local = t_cap, n_cap
        else:
            return None

        hit_local = np.array([ox + dx*t, oy + dy*t, oz + dz*t], dtype=np.float32)
        hit_world = hit_local + np.array([cx, cy, cz], dtype=np.float32)
        normal_world = normalize(n_local)

        return Intercept(point=hit_world, normal=normal_world, distance=t, obj=self)


#   Elipsoide
class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        """
        radii: (rx, ry, rz)
        """
        super().__init__(position, material)
        self.rx, self.ry, self.rz = map(float, radii)
        self.type = "Ellipsoid"

    def ray_intersect(self, orig, dir):
        o = (orig - self.position) / np.array([self.rx, self.ry, self.rz], dtype=np.float32)
        d = dir / np.array([self.rx, self.ry, self.rz], dtype=np.float32)

        a = np.dot(d, d)
        b = 2.0 * np.dot(o, d)
        c = np.dot(o, o) - 1.0

        disc = b*b - 4*a*c
        if disc < 0:
            return None

        rdisc = np.sqrt(disc)
        t0 = (-b - rdisc) / (2*a)
        t1 = (-b + rdisc) / (2*a)

        t = t0 if t0 > EPS else t1
        if t < EPS:
            return None

        p_unit = o + d * t
        hit = self.position + p_unit * np.array([self.rx, self.ry, self.rz], dtype=np.float32)

        # Normal: gradiente de F(x,y,z) = (x/rx)^2 + (y/ry)^2 + (z/rz)^2 - 1
        nx = (hit[0] - self.position[0]) / (self.rx * self.rx)
        ny = (hit[1] - self.position[1]) / (self.ry * self.ry)
        nz = (hit[2] - self.position[2]) / (self.rz * self.rz)
        normal = normalize(np.array([nx, ny, nz], dtype=np.float32))

        return Intercept(point=hit, normal=normal, distance=t, obj=self)


#   Toroide (dona) — cuártico
class Torus(Shape):
    def __init__(self, position, R, r, material):
        super().__init__(position, material)
        self.R = float(R)  # radio mayor
        self.r = float(r)  # radio menor
        self.type = "Torus"

    def ray_intersect(self, orig, dir):
        # Rayo en coords locales del toro
        O = orig - self.position
        D = dir

        ox, oy, oz = O
        dx, dy, dz = D
        R, r = self.R, self.r

        # Coeficientes del cuártico en t
        sum_d_sq = dx*dx + dy*dy + dz*dz
        e = ox*ox + oy*oy + oz*oz - R*R - r*r
        f = ox*dx + oy*dy + oz*dz
        four_R2 = 4.0 * R * R

        coeffs = [
            sum_d_sq*sum_d_sq,
            4.0*sum_d_sq*f,
            2.0*sum_d_sq*e + 4.0*f*f + four_R2*dz*dz,
            4.0*f*e + 2.0*four_R2*oz*dz,
            e*e - four_R2*(r*r - oz*oz)
        ]

        roots = np.roots(coeffs)
        roots = [t.real for t in roots if abs(t.imag) < 1e-6 and t > EPS]
        if not roots:
            return None

        t = min(roots)

        hit_local = O + t * D

        # Gradiente de F(x,y,z) del toroide para la normal
        x, y, z = hit_local
        g = x*x + y*y + z*z - r*r - R*R
        nx = 4.0 * x * g
        ny = 4.0 * y * g
        nz = 4.0 * z * (g + 2.0 * R*R)
        normal_local = normalize(np.array([nx, ny, nz], dtype=np.float32))

        hit_world = hit_local + self.position
        return Intercept(
            point=hit_world,
            normal=normal_local,
            distance=t,
            obj=self,
            texCoords=None,
            rayDirection=dir
        )
