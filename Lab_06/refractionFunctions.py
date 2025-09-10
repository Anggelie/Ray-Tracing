import numpy as np

def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

def refractVector(I: np.ndarray, N: np.ndarray, ior: float) -> np.ndarray | None:
    """
    Devuelve el vector de refracción (normalizado) usando la ley de Snell.
    I: dirección incidente (normalizada)
    N: normal en el punto (normalizada, apuntando hacia fuera)
    ior: índice de refracción del material (ej. vidrio ~1.5)
    Retorna None cuando hay reflexión interna total.
    """
    I = _normalize(I)
    N = _normalize(N)

    cosi = np.clip(np.dot(I, N), -1.0, 1.0)
    etai, etat = 1.0, ior
    n = N.copy()

    # Si estamos dentro del material, invertimos normal e índices
    if cosi > 0:
        etai, etat = etat, etai
        n = -N

    eta = etai / etat
    k = 1.0 - eta * eta * (1.0 - cosi * cosi)
    if k < 0.0:
        # Reflexión interna total
        return None

    t = eta * I - (eta * cosi + np.sqrt(k)) * n
    return _normalize(t)

def fresnel(N: np.ndarray, I: np.ndarray, ior: float) -> float:
    """
    Aproximación de Fresnel (Schlick). Devuelve kr (porcentaje de reflexión),
    y (1-kr) sería el porcentaje de refracción.
    """
    I = _normalize(I)
    N = _normalize(N)

    cosi = np.clip(np.dot(I, N), -1.0, 1.0)
    etai, etat = 1.0, ior

    # Si el rayo viene desde dentro del material
    if cosi > 0:
        etai, etat = etat, etai

    # Comprobamos reflexión interna total
    sint = etai / etat * np.sqrt(max(0.0, 1.0 - cosi * cosi))
    if sint >= 1.0:
        return 1.0

    cost = np.sqrt(max(0.0, 1.0 - sint * sint))
    cosx = cost if cosi > 0 else -cosi

    R0 = ((etai - etat) / (etai + etat)) ** 2
    return float(R0 + (1.0 - R0) * (1.0 - cosx) ** 5)
