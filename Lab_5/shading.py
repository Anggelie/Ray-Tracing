# Shading con sombras

import numpy as np
from math import pow
from vec import Vec3

def phong_shade(point, normal, view_dir, material, lights, ambient=0.1):
    color = np.array(material.color) * ambient
    for light in lights:
        light_dir = np.array(light.direction)
        light_dir = light_dir / np.linalg.norm(light_dir)
        diff = max(np.dot(normal, light_dir), 0)
        color += np.array(material.color) * diff * light.intensity
        reflect_dir = 2 * normal * np.dot(normal, light_dir) - light_dir
        spec = max(np.dot(view_dir, reflect_dir), 0) ** material.shininess
        color += np.array(light.color) * spec * light.intensity * material.specular
    return np.clip(color, 0, 1)
