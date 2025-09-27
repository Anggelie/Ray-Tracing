import numpy as np

# Pequeño epsilon para evitar divisiones por cero 
EPS = 1e-6

# Vectores y operaciones básicas
def vec3(x, y=None, z=None, dtype=np.float32):
    """Crea un vector 3D. Acepta vec/list/np.array o 3 scalars."""
    if y is None and z is None:
        v = np.array(x, dtype=dtype)
        if v.shape != (3,):
            v = v.reshape(3)
        return v.astype(dtype)
    return np.array([x, y, z], dtype=dtype)

def length(v):
    """Norma Euclídea."""
    return float(np.linalg.norm(v))

def dot(a, b):
    """Producto punto."""
    return float(np.dot(a, b))

def cross(a, b):
    """Producto cruz."""
    return np.cross(a, b).astype(np.float32)

def normalize(v):
    """Normaliza un vector (si su norma es ~0, retorna el original)."""
    v = np.asarray(v, dtype=np.float32)
    n = np.linalg.norm(v)
    if n < EPS:
        return v
    return (v / n).astype(np.float32)

def clamp01(x):
    """Clampa un escalar o array al rango [0,1]."""
    return np.clip(x, 0.0, 1.0)

def lerp(a, b, t):
    """Interpolación lineal entre a y b con factor t en [0,1]."""
    return a * (1.0 - t) + b * t

def faceforward(n, v):
    """
    Asegura que la normal n apunte en contra de v (útil para evitar caras traseras).
    Retorna n si dot(n, v) < 0; de lo contrario -n.
    """
    return n if dot(n, v) < 0.0 else -n

def safe_inv(x, eps=EPS):
    """
    Inversa segura: evita división por cero.
    Retorna 1/x si |x|>=eps; si no, 1/(sign(x)*eps).
    """
    x = float(x)
    if abs(x) < eps:
        return 1.0 / (np.sign(x) * eps if x != 0.0 else eps)
    return 1.0 / x

# Reflexión / Refracción 
def reflect(I, N):
    """
    Refleja el vector de incidencia I con respecto a la normal N.
    - I: dirección incidente (apunta *hacia* la superficie)
    - N: normal unitaria
    Retorna: R = I - 2 * dot(I,N) * N
    """
    I = np.asarray(I, dtype=np.float32)
    N = normalize(N)
    return (I - 2.0 * dot(I, N) * N).astype(np.float32)

def refract(I, N, etai, etat):
    """
    Refracción (Snell). Direcciones en convención 'I' entrando a la superficie.

    Parámetros:
    - I: vector incidente (unitario)
    - N: normal unitaria, apuntando hacia el medio 'etai'
    - etai: índice de refracción del medio incidente
    - etat: índice de refracción del medio transmitido

    Retorna vector refractado (unitario). Si hay Reflexión Interna Total,
    retorna vector cero (0,0,0).
    """
    I = normalize(I)
    N = normalize(N)

    cosi = np.clip(dot(I, N), -1.0, 1.0) 
    n1, n2 = float(etai), float(etat)
    n = N.copy()
    if cosi > 0.0:
        n = -N
        n1, n2 = n2, n1
        cosi = -cosi 

    eta = n1 / n2
    k = 1.0 - eta * eta * (1.0 - cosi * cosi)

    if k < 0.0:
        return np.zeros(3, dtype=np.float32)

    T = eta * I + (eta * cosi - np.sqrt(k)) * n
    return normalize(T)

def ortho_basis(n):
    """
    Construye (t, b, n) ortonormales dado n (unitario).
    Devuelve: (tangent, bitangent, normal)
    """
    n = normalize(n)
    if abs(n[1]) < 0.9:
        a = np.array([0, 1, 0], dtype=np.float32)
    else:
        a = np.array([1, 0, 0], dtype=np.float32)
    t = normalize(np.cross(a, n))
    b = normalize(np.cross(n, t))
    return t, b, n

def project(v, n):
    """Proyección de v sobre n (n no necesita estar normalizada)."""
    n2 = dot(n, n)
    if n2 < EPS:
        return np.zeros(3, dtype=np.float32)
    return (dot(v, n) / n2) * np.asarray(n, dtype=np.float32)

def reject(v, n):
    """Componente de v perpendicular a n: v - project(v, n)."""
    return np.asarray(v, dtype=np.float32) - project(v, n)
