import numpy as np
from Textures.MathLib import normalize, reflect, refract
from Textures.intercept import Intercept
from Textures.envmap import EnvMap   

EPS = 1e-4

class Raytracer:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.aspect_ratio = width / height
        self.backgroundColor = np.array([0.93, 0.94, 0.96], dtype=np.float32)

        self.scene  = []
        self.lights = []

        self.envmap = None       
        self.env_intensity = 1.0     

        self.max_depth = 3

        self.eye = np.array([0, 0, 0], dtype=np.float32)
        self.fov = 60
        self.framebuffer = np.zeros((height, width, 3), dtype=np.float32)

    # Bucle de render
    def render(self):
        fov_scale = np.tan(np.radians(self.fov) * 0.5)
        w = self.width; h = self.height

        print("Iniciando render...")
        for j in range(h):
            if h >= 20 and j % (h // 20) == 0:
                print(f"{int(100*j/h)}% ...")
            y_ndc = (1 - 2 * ((j + 0.5) / h))  
            for i in range(w):
                x_ndc = (2 * ((i + 0.5) / w) - 1) * self.aspect_ratio
                direction = normalize(np.array([x_ndc * fov_scale, y_ndc * fov_scale, -1.0], dtype=np.float32))
                self.framebuffer[j, i] = self.cast_ray(self.eye, direction)
        print("100% ... listo!")

    def cast_ray(self, orig, direction, depth=0):
        hit = self.scene_intersect(orig, direction)
        if hit is None:
            if self.envmap is not None:
                return np.clip(self.envmap.sample(direction) * self.env_intensity, 0, 1)
            return self.backgroundColor.copy()

        return self.shade(hit, direction, depth)

    def scene_intersect(self, orig, direction):
        nearest = None
        min_dist = np.inf
        for obj in self.scene:
            h = obj.ray_intersect(orig, direction)
            if h is not None and EPS < h.distance < min_dist:
                nearest = h
                min_dist = h.distance
        return nearest

    def shade(self, hit: Intercept, view_dir, depth):
        m = hit.obj.material
        p = hit.point
        n = normalize(hit.normal)

        # Luz difusa + especular
        color = np.zeros(3, dtype=np.float32)

        for light in self.lights:
            if getattr(light, "type", "") == "AMBIENT":
                color += m.color * light.intensity * m.kd
                continue

            if light.type == "DIRECTIONAL":
                ldir = normalize(-light.direction)
                intensity = light.intensity
                dist_to_light = np.inf
            else: 
                ldir = normalize(light.position - p)
                intensity = light.intensity
                dist_to_light = np.linalg.norm(light.position - p)

            # Sombras (shadow ray)
            shadow_hit = self.scene_intersect(p + n * EPS * 10, ldir)
            if shadow_hit is not None and shadow_hit.distance < dist_to_light:
                continue 

            # Difuso
            diff = max(0.0, np.dot(n, ldir))
            color += m.color * intensity * m.kd * diff

            # Especular
            hdir = normalize(ldir - view_dir)
            spec = max(0.0, np.dot(n, hdir)) ** max(1.0, m.shininess)
            color += np.array([1,1,1], dtype=np.float32) * intensity * m.ks * spec

        # Reflexión
        if m.ks > 0 and depth < self.max_depth:
            rdir = reflect(view_dir, n)
            rcol = self.cast_ray(p + n * EPS * 10, rdir, depth + 1)
            color = (1 - m.ks) * color + m.ks * rcol

        return np.clip(color, 0, 1)
