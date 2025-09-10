import math

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def length(v):
    return math.sqrt(dot(v, v))

def norm(v):
    l = length(v)
    if l == 0: return [0,0,0]
    return [v[0]/l, v[1]/l, v[2]/l]

def add(a, b): return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]
def sub(a, b): return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
def mul(a, s): return [a[0]*s, a[1]*s, a[2]*s]
def hadamard(a, b): return [a[0]*b[0], a[1]*b[1], a[2]*b[2]]

def clamp01(x): return max(0.0, min(1.0, x))

def reflectVector(n, v):
    # v = dirección incidente (desde el punto hacia la cámara/luz)
    # n = normal (normalizada)
    # r = v - 2(n·v)n
    nv = dot(n, v)
    return sub(v, mul(n, 2.0 * nv))

def refractVector(n, v, ior_in, ior_out):
    # v: dirección incidente (normalizada) apuntando haciala superficie
    # n: normal (normalizada) apuntando hacia fuera del objeto
    # devuelve la dirección transmitida 
    eta = ior_in / ior_out
    cosi = -clamp01(dot(n, v))         
    k = 1.0 - eta*eta*(1.0 - cosi*cosi)
    if k < 0.0:
        return None  
    t = add(mul(v, eta), mul(n, (eta*cosi - math.sqrt(k))))
    return norm(t)

def fresnel_schlick(cosTheta, F0):
    return [
        F0[0] + (1.0 - F0[0]) * ((1.0 - cosTheta) ** 5.0),
        F0[1] + (1.0 - F0[1]) * ((1.0 - cosTheta) ** 5.0),
        F0[2] + (1.0 - F0[2]) * ((1.0 - cosTheta) ** 5.0),
    ]
