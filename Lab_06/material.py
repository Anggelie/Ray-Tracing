from MathLib import reflectVector
from refractionFunctions import refractVector, fresnel
from lights import AmbientLight

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse=[1,1,1], spec=32, ks=0.0, ior=1.0, matType=OPAQUE):
        self.diffuse = diffuse     
        self.spec    = spec        
        self.ks      = ks          
        self.ior     = ior        
        self.matType = matType     

    def GetSurfaceColor(self, intercept, renderer, recursion=0):
        """
        Calcula el color en el punto de intersección según el material.
        Usa reflexión, refracción y Fresnel donde corresponda.
        """
        if recursion > renderer.maxRecursionDepth:
            return [0.0, 0.0, 0.0]

        finalColor   = [0.0, 0.0, 0.0]
        lightColor   = [0.0, 0.0, 0.0]
        specColor    = [0.0, 0.0, 0.0]

        if self.matType == OPAQUE:
            for light in renderer.lights:
                if isinstance(light, AmbientLight):
                    lc = light.GetDiffuseColor(intercept, renderer)
                    for i in range(3):
                        lightColor[i] += lc[i]
                else:
                    lc = light.GetDiffuseColor(intercept, renderer)
                    sc = light.GetSpecularColor(intercept, renderer.camera.translation, self.spec)
                    for i in range(3):
                        lightColor[i] += lc[i]
                        specColor[i]  += sc[i] * self.ks

            for i in range(3):
                finalColor[i] = self.diffuse[i] * lightColor[i] + specColor[i]

        elif self.matType == REFLECTIVE:
            reflectDir = reflectVector(intercept.normal, intercept.rayDirection)
            hit = renderer.glCastRay(intercept.point, reflectDir, intercept.obj, recursion+1)
            if hit:
                reflectColor = hit.obj.material.GetSurfaceColor(hit, renderer, recursion+1)
            else:
                reflectColor = renderer.glEnvMap(intercept.point, reflectDir)

            finalColor = reflectColor

        elif self.matType == TRANSPARENT:
            I = intercept.rayDirection
            N = intercept.normal

            # Cálculo del reflejo
            reflectDir = reflectVector(N, I)
            hit = renderer.glCastRay(intercept.point, reflectDir, intercept.obj, recursion+1)
            if hit:
                reflectColor = hit.obj.material.GetSurfaceColor(hit, renderer, recursion+1)
            else:
                reflectColor = renderer.glEnvMap(intercept.point, reflectDir)

            # Cálculo de refracción
            refractDir = refractVector(I, N, self.ior)
            if refractDir is not None:
                hit2 = renderer.glCastRay(intercept.point, refractDir, intercept.obj, recursion+1)
                if hit2:
                    refractColor = hit2.obj.material.GetSurfaceColor(hit2, renderer, recursion+1)
                else:
                    refractColor = renderer.glEnvMap(intercept.point, refractDir)
            else:
                refractColor = [0.0, 0.0, 0.0]

            kr = fresnel(N, I, self.ior)
            finalColor = [
                reflectColor[i] * kr + refractColor[i] * (1 - kr)
                for i in range(3)
            ]

        finalColor = [min(1.0, max(0.0, c)) for c in finalColor]
        return finalColor
