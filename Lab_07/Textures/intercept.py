class Intercept(object):
    def __init__(self, point=None, normal=None, distance=float("inf"),
                 texCoords=None, rayDirection=None, obj=None):
        self.point = point          # np.array([x, y, z])
        self.normal = normal        # np.array([nx, ny, nz]) UNIDAD
        self.distance = distance    # t
        self.texCoords = texCoords 
        self.rayDirection = rayDirection
        self.obj = obj              # referencia al objeto intersectado
