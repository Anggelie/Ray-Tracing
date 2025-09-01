# shading.py
import numpy as np

_EPS = 1e-4

def _reflect(I, N):
    # R = I - 2(N·I)N   (I entra hacia la superficie)
    return I - 2.0*np.dot(N, I)*N

def _occluded(scene, origin, dir, max_t):
    # Ray de sombra: chequea si hay cualquier hit antes de llegar a la luz
    for obj in scene:
        hit = obj.ray_intersect(origin, dir)
        if hit is None:
            continue
        t, _, _, _ = hit
        if _EPS < t < max_t - _EPS:
            return True
    return False

def phong_shade(P, N, V, mat, lights, ambient_intensity, scene=None):
    """
    P: punto de intersección (np.array 3)
    N: normal en P (np.array 3, normalizada)
    V: dirección hacia el ojo (np.array 3, normalizada)
    mat: Material (color, specular, shininess)
    lights: [Light...]
    ambient_intensity: float (0..1)
    scene: lista de objetos para sombras (opcional)
    """
    N = N / (np.linalg.norm(N) + 1e-8)
    V = V / (np.linalg.norm(V) + 1e-8)

    # Ambient
    final = np.array(mat.color) * ambient_intensity

    for L in lights:
        if getattr(L, "light_type", "Directional") == "Ambient":
            final += np.array(mat.color) * L.energy()
            continue

        if getattr(L, "light_type", "Directional") == "Directional":
            Ldir = -np.array(L.direction, dtype=float)
            Ldir /= (np.linalg.norm(Ldir) + 1e-8)
            dist = np.inf
            light_energy = L.energy()

        elif getattr(L, "light_type", "Directional") == "Point":
            to_light = np.array(L.position, dtype=float) - P
            dist = np.linalg.norm(to_light)
            if dist < _EPS:
                continue
            Ldir = to_light / dist
            light_energy = L.energy() * L.attenuation(dist)

        else:
            continue

        # Sombras
        if scene is not None:
            shadow_origin = P + N * _EPS
            max_t = dist if np.isfinite(dist) else 1e8
            if _occluded(scene, shadow_origin, Ldir, max_t):
                continue  # en sombra: omite difusa/especular

        # Difusa (Lambert)
        diff = max(0.0, float(np.dot(N, Ldir)))

        # Especular (Phong)
        R = _reflect(-Ldir, N)
        spec = max(0.0, float(np.dot(R, V))) ** max(1, mat.shininess)

        # Acumula luz
        final += (np.array(mat.color) * diff + mat.specular * spec) * light_energy

    # Clamp 0..1
    return np.clip(final, 0.0, 1.0)
