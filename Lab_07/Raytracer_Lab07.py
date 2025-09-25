import numpy as np
from BMP.BMP_Writer import save as save_bmp
from Textures.gl import Raytracer
from Textures.material import Material, MAT_DIFFUSE, MAT_REFLECTIVE
from Textures.lights import AmbientLight, DirectionalLight, PointLight
from Textures.figures import Plane, Disk, Triangle, Cube
from Textures.MathLib import normalize

def main():
    width = 800
    height = 600
    
    # Configuración para mejor calidad de sombras e iluminación
    rt = Raytracer(width, height, 
                   samples_per_pixel=6,     
                   enable_ao=True,          
                   ao_samples=12,           
                   ao_distance=3.0,         
                   max_depth=4)             

    rt.eye = np.array([2.5, 2.8, 4.2], dtype=np.float32)
    rt.target = np.array([0, -0.2, -0.5], dtype=np.float32)
    rt.up = np.array([0, 1, 0], dtype=np.float32)
    rt.fov = 55.0

    def hexc(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

    Tangerine = hexc('#F08C21')  
    Butter    = hexc('#F2D88F')  
    Blush     = hexc('#E36888')  
    Sea       = hexc('#6698CC') 
    Matcha    = hexc('#B4B534')  

    WallWhite = (0.95, 0.95, 0.95)
    FloorBeige = (0.85, 0.80, 0.72)

    wallMaterial = Material(color=WallWhite, kd=0.85, ks=0.05, shininess=15, mtype=MAT_DIFFUSE)
    floorMaterial = Material(color=FloorBeige, kd=0.7, ks=0.3, shininess=60, mtype=MAT_REFLECTIVE)
    
    cubeSeaMaterial = Material(color=Sea, kd=0.8, ks=0.2, shininess=50, mtype=MAT_DIFFUSE)
    cubeBlushMaterial = Material(color=Blush, kd=0.8, ks=0.2, shininess=50, mtype=MAT_DIFFUSE)
    triangleMatchaMaterial = Material(color=Matcha, kd=0.85, ks=0.15, shininess=40, mtype=MAT_DIFFUSE)
    diskTangerineMaterial = Material(color=Tangerine, kd=0.8, ks=0.2, shininess=45, mtype=MAT_DIFFUSE)

    rt.scene = [
        Plane(position=(0, -1, 0),   normal=(0, 1, 0),  material=floorMaterial),   # Piso con reflexión
        Plane(position=(0, 4, 0),    normal=(0, -1, 0), material=wallMaterial),    # Techo
        Plane(position=(0, 0, -3.5), normal=(0, 0, 1),  material=wallMaterial),    # Pared fondo
        Plane(position=(-3, 0, 0),   normal=(1, 0, 0),  material=wallMaterial),    # Pared izquierda
        Plane(position=(3, 0, 0),    normal=(-1, 0, 0), material=wallMaterial),    # Pared derecha
        

        Cube(
            tuple(np.array((-1.3, -0.4, -0.3)) - 0.6),
            tuple(np.array((-1.3, -0.4, -0.3)) + 0.6),
            cubeSeaMaterial
        ),
        
        Cube(
            tuple(np.array((1.3, -0.4, -0.3)) - 0.6),
            tuple(np.array((1.3, -0.4, -0.3)) + 0.6),
            cubeBlushMaterial
        ),
        
        Triangle(
            A=(0, -1, -2),
            B=(-0.5, 1.5, -2.2),
            C=(0.5, 1.5, -2.2),
            material=triangleMatchaMaterial
        ),
        
        Disk(
            position=(0, -0.98, 1.2),
            normal=normalize(np.array([0, 1, 0.02])),
            radius=0.7,
            material=diskTangerineMaterial
        )
    ]

    rt.lights = [
        AmbientLight(color=(1.0, 1.0, 1.0), intensity=0.12),
                DirectionalLight(
            direction=normalize([-0.4, -1.0, -0.3]), 
            color=(1.0, 0.98, 0.95), 
            intensity=0.9
        ),
        
        DirectionalLight(
            direction=normalize([0.6, -0.8, -0.2]), 
            color=(0.95, 0.97, 1.0), 
            intensity=0.4
        ),
        
        PointLight(
            position=[0, 3.2, 0.5], 
            color=(1.0, 0.99, 0.97), 
            intensity=0.7
        ),
        
        PointLight(
            position=[0, 1.5, -2.8], 
            color=(0.98, 0.96, 1.0), 
            intensity=0.3
        )
    ]

    rt.backgroundColor = np.array([0.08, 0.08, 0.08], dtype=np.float32)

    print("Renderizando...")
    rt.render()
    
    print("Guardando render final...")
    save_bmp("renders/Lab07_Final.bmp", rt.width, rt.height, rt.framebuffer)
    print("Completado: Lab07_Final.bmp")

if __name__ == "__main__":
    main()