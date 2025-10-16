import numpy as np

EPS = 1e-8

def length(v):
    """Magnitud de un vector."""
    return float(np.linalg.norm(v))

def normalize(v):
    """Normaliza un vector. Si es vector cero, retorna vector cero."""
    v = np.asarray(v, dtype=np.float32)
    n = np.linalg.norm(v)
    if n < EPS:
        return np.zeros_like(v, dtype=np.float32)
    return (v / n).astype(np.float32)

def dot(a, b):
    """Producto punto entre dos vectores."""
    return float(np.dot(np.asarray(a), np.asarray(b)))

def cross(a, b):
    """Producto cruz entre dos vectores."""
    return np.cross(np.asarray(a), np.asarray(b)).astype(np.float32)

def clamp(x, lo=0.0, hi=1.0):
    """Limita un valor entre lo y hi."""
    return float(max(lo, min(hi, x)))

def reflect(I, N):
    """
    Refleja el vector incidente I respecto a la normal N.
    Fórmula: R = I - 2(I·N)N
    
    Args:
        I: Vector incidente (dirección del rayo)
        N: Normal de la superficie
    
    Returns:
        Vector reflejado normalizado
    """
    I = normalize(np.asarray(I, dtype=np.float32))
    N = normalize(np.asarray(N, dtype=np.float32))
    
    R = I - 2.0 * dot(I, N) * N
    return normalize(R)

def refract(I, N, eta_ratio):
    """
    Calcula la refracción usando la ley de Snell.
    
    Args:
        I: Vector incidente normalizado
        N: Normal de la superficie normalizada
        eta_ratio: Razón de índices de refracción (n1/n2)
    
    Returns:
        Vector refractado normalizado o None si hay reflexión total interna
    """
    I = normalize(np.asarray(I, dtype=np.float32))
    N = normalize(np.asarray(N, dtype=np.float32))
    
    cosi = -dot(I, N)
    cosi = clamp(cosi, -1.0, 1.0)
    
    k = 1.0 - eta_ratio * eta_ratio * (1.0 - cosi * cosi)
    
    if k < 0:
        return None
    
    T = eta_ratio * I + (eta_ratio * cosi - np.sqrt(k)) * N
    return normalize(T)

def fresnel(I, N, ior):
    """
    Ecuaciones de Fresnel - calcula reflectancia.
    
    Args:
        I: Vector incidente
        N: Normal
        ior: Índice de refracción
    
    Returns:
        Coeficiente de reflexión [0, 1]
    """
    cosi = clamp(dot(I, N), -1.0, 1.0)
    etai, etat = 1.0, ior
    
    if cosi > 0:
        etai, etat = etat, etai
    
    sint = etai / etat * np.sqrt(max(0.0, 1.0 - cosi * cosi))
    
    if sint >= 1.0:
        return 1.0
    
    cost = np.sqrt(max(0.0, 1.0 - sint * sint))
    cosi = abs(cosi)
    
    # Ecuaciones de Fresnel
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    
    return (Rs * Rs + Rp * Rp) / 2.0

def lerp(a, b, t):
    """Interpolación lineal entre a y b."""
    t = clamp(t, 0.0, 1.0)
    return a + t * (b - a)

def smoothstep(edge0, edge1, x):
    """Interpolación suave (Hermite)."""
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)