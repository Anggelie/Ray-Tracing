import numpy as np
from .MathLib import vec3, normalize, dot, clamp01, EPS, faceforward
from .intercept import Intercept
from .material import MAT_DIFFUSE
from .lights import AmbientLight, DirectionalLight, PointLight

class Raytracer(object):
    def __init__(self, width, height, samples_per_pixel=4, enable_ao=True, ao_samples=8, ao_distance=1.0, max_depth=3):
        self.width  = int(width)
        self.height = int(height)
        self.clearColor = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.backgroundColor = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.framebuffer = np.zeros((self.height, self.width, 3), dtype=np.float32)

        # Cámara
        self.fov = 60.0
        self.eye = np.array([0, 1.5, 6], dtype=np.float32)  # posición cámara mirando -Z
        self.target = np.array([0, 1, 0], dtype=np.float32)
        self.up = np.array([0, 1, 0], dtype=np.float32)

        self.scene = []
        self.lights = []

        # Sombras y calidad
        self.enable_shadows = True
        self.samples_per_pixel = int(samples_per_pixel) if samples_per_pixel >= 1 else 1
        self.enable_ao = bool(enable_ao)
        self.ao_samples = int(max(1, ao_samples))
        self.ao_distance = float(ao_distance)
        self.max_depth = int(max_depth)
        self._rng = np.random.default_rng()

    def _build_camera_basis(self):
        f = normalize(self.target - self.eye)  
        r = normalize(np.cross(f, self.up))   
        u = np.cross(r, f)                    
        return f, r, u

    def _ray_from_camera(self, x, y):
        f, r, u = self._build_camera_basis()
        aspect = self.width / self.height
        angle = np.tan(np.deg2rad(self.fov * 0.5))
        px = (2 * ((x + 0.5) / self.width)  - 1) * angle * aspect
        py = (1 - 2 * ((y + 0.5) / self.height)) * angle

        # Direccion en espacio de la cámara
        dir_cam = normalize(px * r + py * u + f)
        return self.eye, dir_cam

    def add_object(self, obj):
        self.scene.append(obj)

    def add_light(self, lt):
        self.lights.append(lt)

    def _closest_intersection(self, O, D):
        best = None
        min_t = float("inf")
        for obj in self.scene:
            hit = obj.ray_intersect(O, D)
            if hit is not None and hit.distance < min_t:
                min_t = hit.distance
                best = hit
        return best

    def _hemisphere_sample(self, N):
        u1 = self._rng.random()
        u2 = self._rng.random()
        r = np.sqrt(u1)
        theta = 2 * np.pi * u2
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.sqrt(max(0.0, 1.0 - u1))
        if abs(N[0]) > abs(N[1]):
            tangent = np.array([N[2], 0, -N[0]], dtype=np.float32)
        else:
            tangent = np.array([0, -N[2], N[1]], dtype=np.float32)
        tangent = tangent / np.linalg.norm(tangent)
        bitangent = np.cross(N, tangent)
        sample = x * tangent + y * bitangent + z * N
        return sample / np.linalg.norm(sample)

    def _ambient_occlusion(self, inter):
        if not self.enable_ao:
            return 1.0
        N = inter.normal
        P = inter.point + N * 1e-3
        hits = 0
        for _ in range(self.ao_samples):
            dir_ao = self._hemisphere_sample(N)
            hit = self._closest_intersection(P, dir_ao)
            if hit is not None and hit.distance < self.ao_distance:
                hits += 1
        occ = hits / float(self.ao_samples)
        return max(0.0, 1.0 - occ * 0.7)

    def _in_shadow(self, point, N, light):
        if isinstance(light, AmbientLight):
            return False
        if isinstance(light, PointLight):
            L = normalize(light.position - point)
            maxDist = np.linalg.norm(light.position - point)
        else:
            L = normalize(-light.direction)
            maxDist = float("inf")
        shadowOrig = point + N * 1e-3
        t_hit = self._closest_intersection(shadowOrig, L)
        if t_hit is None:
            return False
        return t_hit.distance < maxDist

    #  Shading
    def _shade(self, inter, rayDir):
        material = inter.obj.material
        viewDir = normalize(-rayDir)
        N = inter.normal

        color = np.zeros(3, dtype=np.float32)

        for lt in self.lights:
            if isinstance(lt, AmbientLight):
                color += lt.GetLightColor() * material.color * material.kd
                continue

            if self.enable_shadows and self._in_shadow(inter.point, N, lt):
                continue

            # Difuso
            diff = lt.GetLightColor(inter=inter, viewDir=viewDir)
            diff_contrib = diff * material.color * material.kd
            color += diff_contrib

            # Especular
            spec = lt.GetSpecularColor(inter=inter, viewDir=viewDir)
            color += spec * material.ks

        ao = self._ambient_occlusion(inter)
        color = color * ao
        return clamp01(color)

    def _trace_ray(self, O, D, depth=0):
        if depth > self.max_depth:
            return self.backgroundColor

        inter = self._closest_intersection(O, D)
        if inter is None:
            return self.backgroundColor

        # Sombra y shading local
        inter.normal = normalize(inter.normal)
        local_color = self._shade(inter, D)

        mat = inter.obj.material
        if getattr(mat, 'mtype', None) == 1:  # MAT_REFLECTIVE
            from .MathLib import reflect
            R = reflect(D, inter.normal)
            # pequeño offset para evitar acne
            newOrig = inter.point + inter.normal * 1e-3
            reflect_color = self._trace_ray(newOrig, R, depth + 1)
            kr = getattr(mat, 'ks', 0.5)
            return clamp01(local_color * (1.0 - kr) + reflect_color * kr)

        return local_color

    # Render 
    def clear(self, r, g, b):
        self.clearColor = np.array([r, g, b], dtype=np.float32)
        self.framebuffer[:] = self.clearColor

    def render(self):
        total = self.height
        for y in range(self.height):
            # progreso cada 10%
            if y % max(1, int(self.height/10)) == 0:
                pct = int(100.0 * y / self.height)
                print(f"Render progress: {pct}%")

            for x in range(self.width):
                accum = np.zeros(3, dtype=np.float32)
                for s in range(self.samples_per_pixel):
                    rx = (self._rng.random() - 0.5)
                    ry = (self._rng.random() - 0.5)
                    sx = float(x) + 0.5 + rx
                    sy = float(y) + 0.5 + ry
                    O, D = self._ray_from_camera(sx, sy)
                    # Usar trazado recursivo para permitir reflexiones
                    col = self._trace_ray(O, D, depth=0)
                    accum += col
                color = accum / float(self.samples_per_pixel)
                gamma = 1.0 / 2.2
                color = np.clip(np.power(color, gamma), 0.0, 1.0)
                self.framebuffer[y, x] = color
