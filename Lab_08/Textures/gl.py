import math
import numpy as np

from Textures.MathLib import normalize, reflect as reflect_vec, refract as refract_vec
from Textures.material import (
    MAT_DIFFUSE,
    MAT_REFLECTIVE,
    MAT_REFRACTIVE,   
)

EPS = 1e-4

def length(v):
    return float(np.linalg.norm(v))

def clamp01(x):
    return max(0.0, min(1.0, float(x)))

def to_np3(x):
    return np.array(x, dtype=np.float32)

# Raytracer  
class Raytracer:
    def __init__(
        self,
        width,
        height,
        samples_per_pixel=1,
        enable_ao=False,
        ao_samples=8,
        ao_distance=2.0,
        max_depth=2,
    ):
        self.width = int(width)
        self.height = int(height)

        # Framebuffer RGB en float
        self.framebuffer = np.zeros((self.height, self.width, 3), dtype=np.float32)

        # Cámara 
        self.eye = to_np3([0, 0, 5])
        self.target = to_np3([0, 0, 0])
        self.up = to_np3([0, 1, 0])
        self.fov = 60.0  # grados

        # Escena y luces
        self.scene = []  
        self.lights = []  

        # Fondo
        self.backgroundColor = to_np3([0.0, 0.0, 0.0])

        # Render options
        self.samples_per_pixel = max(1, int(samples_per_pixel))
        self.enable_ao = bool(enable_ao)
        self.ao_samples = int(ao_samples)
        self.ao_distance = float(ao_distance)
        self.max_depth = int(max_depth)

        # precálculo del frustum
        self._update_camera()

    # Cámara
    def _update_camera(self):
        """Construye base de cámara y escala de la proyección."""
        self.forward = normalize(self.target - self.eye)
        self.right = normalize(np.cross(self.forward, self.up))
        self.true_up = normalize(np.cross(self.right, self.forward))

        # tamaño del plano de proyección en espacio cámara
        aspect = self.width / self.height
        scale = math.tan(math.radians(self.fov) * 0.5)
        self.half_w = aspect * scale
        self.half_h = scale

    def update_camera(self):
        self._update_camera()

    def render(self):
        self._update_camera()

        spp = self.samples_per_pixel
        inv_w = 1.0 / (self.width - 1)
        inv_h = 1.0 / (self.height - 1)

        for y in range(self.height):
            if self.height >= 20 and y % (self.height // 20 or 1) == 0:
                print(f"{int(100*y/self.height)}% ...")

            for x in range(self.width):
                col = np.zeros(3, dtype=np.float32)

                for s in range(spp):
                    jx = (np.random.rand() - 0.5) if spp > 1 else 0.0
                    jy = (np.random.rand() - 0.5) if spp > 1 else 0.0

                    u = ((x + 0.5 + jx) * inv_w) * 2.0 - 1.0
                    v = (1.0 - (y + 0.5 + jy) * inv_h) * 2.0 - 1.0

                    dir_cam = normalize(self.forward +
                                        self.right * (u * self.half_w) +
                                        self.true_up * (v * self.half_h))

                    col += self.cast_ray(self.eye, dir_cam, depth=0)

                self.framebuffer[y, x] = np.clip(col / spp, 0.0, 1.0)

        print("100% ... listo!")

    # Intersección más cercana
    def _closest_hit(self, orig, dir, skip_obj=None):
        closest_t = float("inf")
        closest_hit = None

        for obj in self.scene:
            if skip_obj is not None and obj is skip_obj:
                continue
            hit = obj.ray_intersect(orig, dir)
            if hit is None:
                continue
            if hit.distance < closest_t and hit.distance > EPS:
                closest_t = hit.distance
                closest_hit = hit

        return closest_hit


    def _ambient_occlusion(self, p, n):
        if not self.enable_ao or self.ao_samples <= 0:
            return 1.0

        occluded = 0
        for _ in range(self.ao_samples):
            xi1 = np.random.rand()
            xi2 = np.random.rand()
            r = math.sqrt(xi1)
            theta = 2.0 * math.pi * xi2
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = math.sqrt(max(0.0, 1.0 - xi1))

            up = np.array([0, 1, 0], dtype=np.float32)
            if abs(np.dot(up, n)) > 0.9:
                up = np.array([1, 0, 0], dtype=np.float32)
            t = normalize(np.cross(up, n))
            b = normalize(np.cross(n, t))

            dir_hemi = normalize(t * x + b * y + n * z)

            hit = self._closest_hit(p + n * EPS * 2.0, dir_hemi)
            if hit is not None and hit.distance < self.ao_distance:
                occluded += 1

        return 1.0 - (occluded / self.ao_samples)

    # Sombreado
    def cast_ray(self, orig, dir, depth=0):
        hit = self._closest_hit(orig, dir)
        if hit is None:
            return self.backgroundColor.copy()

        p = hit.point
        n = normalize(hit.normal)
        m = hit.obj.material
        ao = self._ambient_occlusion(p, n)

        # Iluminación directa
        color = np.zeros(3, dtype=np.float32)

        for L in self.lights:
            if L.type == "Ambient":
                color += ao * L.color * L.intensity * m.kd * np.array(m.color, dtype=np.float32)
                continue

            # vector luz y atenuación
            if L.type == "Directional":
                ldir = normalize(-to_np3(L.direction))
                distance_to_light = float("inf")
                attenuation = 1.0
            else:  # Point
                Lpos = to_np3(L.position)
                vecL = Lpos - p
                distance_to_light = length(vecL)
                ldir = normalize(vecL)
                # atenuación simple cuadrática
                attenuation = 1.0 / (1.0 + 0.09 * distance_to_light + 0.032 * distance_to_light * distance_to_light)

            # Sombras (shadow ray)
            shadow_hit = self._closest_hit(p + n * EPS * 3.0, ldir, skip_obj=None)
            if shadow_hit is not None:
                if L.type == "Directional" or shadow_hit.distance < distance_to_light - EPS:
                    continue  # en sombra

            # Diffuse
            ndotl = clamp01(np.dot(n, ldir))
            diffuse = m.kd * ndotl * np.array(m.color, dtype=np.float32)

            # Specular
            view_dir = normalize(orig - p)
            if L.type == "Directional":
                light_dir = ldir
            else:
                light_dir = ldir
            half_vec = normalize(light_dir + view_dir)
            spec = pow(clamp01(np.dot(n, half_vec)), max(1.0, float(m.shininess)))
            specular = m.ks * spec * np.ones(3, dtype=np.float32)

            color += (diffuse + specular) * L.color * L.intensity * attenuation

        # Reflexión / refracción
        if depth < self.max_depth:
            if m.mtype == MAT_REFLECTIVE:
                rdir = normalize(reflect_vec(dir, n))
                rcol = self.cast_ray(p + n * EPS * 4.0, rdir, depth + 1)
                color = (1.0 - m.ks) * color + m.ks * rcol

            elif 'MAT_REFRACTIVE' in globals() and m.mtype == MAT_REFRACTIVE:
                ior = getattr(m, "ior", 1.3)
                cosi = clamp01(-np.dot(n, dir))
                etai, etat = (1.0, ior) if cosi > 0 else (ior, 1.0)
                eta = etai / etat
                k = 1.0 - eta * eta * (1.0 - cosi * cosi)
                if k < 0:
                    rdir = normalize(reflect_vec(dir, n))
                    color = self.cast_ray(p + n * EPS * 4.0, rdir, depth + 1)
                else:
                    tdir = normalize(refract_vec(dir, n, etai, etat))
                    rdir = normalize(reflect_vec(dir, n))
                    rcol = self.cast_ray(p + n * EPS * 4.0, rdir, depth + 1)
                    tcol = self.cast_ray(p - n * EPS * 4.0, tdir, depth + 1)
                    fresnel = self._fresnel(cosi, etai, etat)
                    color = rcol * fresnel + tcol * (1.0 - fresnel) * m.kd

        return np.clip(color, 0.0, 1.0)

    def _fresnel(self, cosi, etai, etat):
        r0 = ((etai - etat) / (etai + etat)) ** 2
        return r0 + (1.0 - r0) * ((1.0 - cosi) ** 5)
 