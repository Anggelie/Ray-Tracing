import numpy as np
from Textures.MathLib import normalize
from Textures.intercept import Intercept
from Textures.material import Material

EPS = 1e-6

# Base
class Shape:
    def __init__(self, position, material: Material):
        self.position = np.array(position, dtype=np.float32) if position is not None else None
        self.material = material
        self.type = "Shape"

    def ray_intersect(self, orig, dir):
        raise NotImplementedError

# Esfera 
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

# Plano
class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normalize(np.array(normal, dtype=np.float32))
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        if abs(denom) < EPS:
            return None
            
        t = np.dot(self.position - orig, self.normal) / denom
        if t < EPS:
            return None
            
        hit = orig + dir * t
        return Intercept(point=hit, normal=self.normal, distance=t, obj=self)

# Disco
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
        if np.dot(v, v) <= self.radius * self.radius:
            return plane_hit
        return None

#  Triángulo
class Triangle(Shape):
    def __init__(self, A, B, C, material):
        super().__init__(A, material)
        self.A = np.array(A, dtype=np.float32)
        self.B = np.array(B, dtype=np.float32)
        self.C = np.array(C, dtype=np.float32)
        
        # Calcular normal
        edge1 = self.B - self.A
        edge2 = self.C - self.A
        self.normal = normalize(np.cross(edge1, edge2))
        self.type = "Triangle"

    def ray_intersect(self, orig, dir):
        edge1 = self.B - self.A
        edge2 = self.C - self.A
        
        h = np.cross(dir, edge2)
        a = np.dot(edge1, h)
        
        if abs(a) < EPS:
            return None  # Rayo paralelo al triángulo
            
        f = 1.0 / a
        s = orig - self.A
        u = f * np.dot(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
            
        q = np.cross(s, edge1)
        v = f * np.dot(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None
            
        t = f * np.dot(edge2, q)
        
        if t < EPS:
            return None
            
        hit = orig + dir * t
        return Intercept(point=hit, normal=self.normal, distance=t, obj=self)

# AABB (Cubo)
class Cube(Shape):
    def __init__(self, min_point, max_point, material):
        super().__init__(min_point, material)
        self.min = np.array(min_point, dtype=np.float32)
        self.max = np.array(max_point, dtype=np.float32)
        self.type = "Cube"

    def ray_intersect(self, orig, dir):
        # Algoritmo de intersección AABB optimizado
        inv_dir = 1.0 / (dir + EPS * np.sign(dir))
        
        t_min = (self.min - orig) * inv_dir
        t_max = (self.max - orig) * inv_dir
        
        t1 = np.minimum(t_min, t_max)
        t2 = np.maximum(t_min, t_max)
        
        t_near = np.max(t1)
        t_far = np.min(t2)
        
        if t_near > t_far or t_far < EPS:
            return None
            
        t = t_near if t_near > EPS else t_far
        if t < EPS:
            return None
            
        hit = orig + dir * t
        
        # Calcular normal basada en la cara impactada
        center = (self.min + self.max) * 0.5
        local_hit = hit - center
        half_size = (self.max - self.min) * 0.5
        
        # Encontrar la componente con mayor valor absoluto normalizado
        normalized = local_hit / (half_size + EPS)
        abs_normalized = np.abs(normalized)
        max_idx = np.argmax(abs_normalized)
        
        normal = np.zeros(3, dtype=np.float32)
        normal[max_idx] = np.sign(normalized[max_idx])
        
        return Intercept(point=hit, normal=normal, distance=t, obj=self)

# Cilindro (con UV)
class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = float(radius)
        self.height = float(height)
        self.type = "Cylinder"

    def ray_intersect(self, orig, dir):
        # Transformar a espacio local del cilindro
        local_orig = orig - self.position
        
        # Componentes del rayo en el plano XZ
        ox, oy, oz = local_orig
        dx, dy, dz = dir
        
        # Cilindro infinito en Y
        a = dx * dx + dz * dz
        b = 2.0 * (ox * dx + oz * dz)
        c = ox * ox + oz * oz - self.radius * self.radius
        
        y_min = -self.height * 0.5
        y_max = self.height * 0.5
        
        t_side = None
        normal_side = None
        texcoords = None
        
        # Intersección con la superficie lateral
        if abs(a) > EPS:
            disc = b * b - 4 * a * c
            if disc >= 0:
                sqrt_disc = np.sqrt(disc)
                t0 = (-b - sqrt_disc) / (2 * a)
                t1 = (-b + sqrt_disc) / (2 * a)
                
                for t_candidate in [t0, t1]:
                    if t_candidate > EPS:
                        y_hit = oy + dy * t_candidate
                        if y_min <= y_hit <= y_max:
                            t_side = t_candidate
                            
                            # Normal lateral (perpendicular al eje Y)
                            hit_local = local_orig + dir * t_side
                            normal_local = np.array([hit_local[0], 0.0, hit_local[2]], dtype=np.float32)
                            normal_side = normalize(normal_local)
                            
                            # UV mapping lateral
                            theta = np.arctan2(hit_local[2], hit_local[0])
                            u = (theta / (2.0 * np.pi)) + 0.5
                            v = (y_hit - y_min) / self.height
                            texcoords = (float(u), float(v))
                            break
        
        # Intersección con las tapas
        t_cap = None
        normal_cap = None
        
        if abs(dy) > EPS:
            # Tapa superior
            t_top = (y_max - oy) / dy
            if t_top > EPS:
                x_hit = ox + dx * t_top
                z_hit = oz + dz * t_top
                if x_hit * x_hit + z_hit * z_hit <= self.radius * self.radius:
                    if t_side is None or t_top < t_side:
                        t_cap = t_top
                        normal_cap = np.array([0.0, 1.0, 0.0], dtype=np.float32)
            
            # Tapa inferior
            t_bottom = (y_min - oy) / dy
            if t_bottom > EPS:
                x_hit = ox + dx * t_bottom
                z_hit = oz + dz * t_bottom
                if x_hit * x_hit + z_hit * z_hit <= self.radius * self.radius:
                    if (t_cap is None or t_bottom < t_cap) and (t_side is None or t_bottom < t_side):
                        t_cap = t_bottom
                        normal_cap = np.array([0.0, -1.0, 0.0], dtype=np.float32)
        
        # Elegir la intersección más cercana
        if t_side is None and t_cap is None:
            return None
            
        if t_cap is None or (t_side is not None and t_side < t_cap):
            hit = orig + dir * t_side
            return Intercept(point=hit, normal=normal_side, distance=t_side, 
                           texcoords=texcoords, obj=self)
        else:
            hit = orig + dir * t_cap
            return Intercept(point=hit, normal=normal_cap, distance=t_cap, obj=self)

# Elipsoide
class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        super().__init__(position, material)
        self.radii = np.array(radii, dtype=np.float32)
        self.rx, self.ry, self.rz = self.radii
        self.type = "Ellipsoid"

    def ray_intersect(self, orig, dir):
        # Transformar a espacio de esfera unitaria
        scale = 1.0 / self.radii
        o_scaled = (orig - self.position) * scale
        d_scaled = dir * scale
        
        # Intersección con esfera unitaria
        a = np.dot(d_scaled, d_scaled)
        b = 2.0 * np.dot(o_scaled, d_scaled)
        c = np.dot(o_scaled, o_scaled) - 1.0
        
        disc = b * b - 4 * a * c
        if disc < 0:
            return None
            
        sqrt_disc = np.sqrt(disc)
        t0 = (-b - sqrt_disc) / (2 * a)
        t1 = (-b + sqrt_disc) / (2 * a)
        
        t = t0 if t0 > EPS else t1
        if t < EPS:
            return None
            
        # Punto de impacto en espacio original
        hit = orig + dir * t
        
        # Normal del elipsoide: gradiente de la ecuación implícita
        # Para (x²/rx² + y²/ry² + z²/rz² - 1 = 0)
        # ∇f = (2x/rx², 2y/ry², 2z/rz²)
        local = hit - self.position
        normal_local = local / (self.radii * self.radii)
        normal = normalize(normal_local)
        
        return Intercept(point=hit, normal=normal, distance=t, obj=self)

# Toro (cuártico)
class Torus(Shape):
    def __init__(self, position, R, r, material):
        super().__init__(position, material)
        self.R = float(R)  # Radio mayor (centro del tubo)
        self.r = float(r)  # Radio menor (radio del tubo)
        self.type = "Torus"

    def ray_intersect(self, orig, dir):
        # Transformar a espacio local
        local_orig = orig - self.position
        
        ox, oy, oz = local_orig
        dx, dy, dz = dir
        
        R, r = self.R, self.r
        
        # Coeficientes del polinomio cuártico
        sum_d_sq = dx*dx + dy*dy + dz*dz
        e = ox*ox + oy*oy + oz*oz - R*R - r*r
        f = ox*dx + oy*dy + oz*dz
        four_R2 = 4.0 * R * R
        
        # at⁴ + bt³ + ct² + dt + e = 0
        coeffs = [
            sum_d_sq * sum_d_sq,                                   
            4.0 * sum_d_sq * f,                                    
            2.0 * sum_d_sq * e + 4.0 * f * f + four_R2 * dy * dy,  
            4.0 * f * e + 2.0 * four_R2 * oy * dy,                
            e * e - four_R2 * (r * r - oy * oy)               
        ]
        
        # Resolver polinomio cuártico
        try:
            roots = np.roots(coeffs)
        except:
            return None
            
        valid_roots = []
        for root in roots:
            if abs(root.imag) < EPS and root.real > EPS:
                valid_roots.append(root.real)
        
        if not valid_roots:
            return None
            
        t = min(valid_roots)
        hit_local = local_orig + dir * t
        
        # Calcular normal 
        # Normal = gradiente de f(x,y,z) = (x²+y²+z²+R²-r²)² - 4R²(x²+z²)
        x, y, z = hit_local
        
        # Término auxiliar
        sum_sq = x*x + y*y + z*z
        Q = sum_sq + R*R - r*r
        
        # Gradiente
        nx = 4.0 * x * Q - 8.0 * R * R * x
        ny = 4.0 * y * Q
        nz = 4.0 * z * Q - 8.0 * R * R * z
        
        normal = normalize(np.array([nx, ny, nz], dtype=np.float32))
        hit = hit_local + self.position
        
        return Intercept(point=hit, normal=normal, distance=t, obj=self)