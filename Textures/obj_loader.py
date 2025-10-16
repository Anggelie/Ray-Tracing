# En esta parte le pedi ayuda a ChatGPT, porque no sabía si estaba corriendo correctamnete mi modelo, entonces son como avisos de que ya esta funcionando
import numpy as np
from Textures.figures import Triangle
from Textures.MathLib import normalize

class OBJModel:
    """
    Carga un archivo .obj y genera triángulos para ray tracing.
    Soporta múltiples materiales.
    """
    
    def __init__(self, filepath, material=None, materials_dict=None, 
                 scale=1.0, position=(0, 0, 0), rotation=(0, 0, 0)):
        """
        Args:
            filepath: Ruta al archivo .obj
            material: Material por defecto (si no se usa materials_dict)
            materials_dict: Dict de materiales por nombre, ej: {'Bark': mat1, 'Tree': mat2}
            scale: Escala del modelo (float o tuple de 3 valores)
            position: Posición (x, y, z) del modelo en la escena
            rotation: Rotación (rx, ry, rz) en grados
        """
        self.filepath = filepath
        self.default_material = material
        self.materials_dict = materials_dict or {}
        
        # Manejar escala como float o tuple
        if isinstance(scale, (int, float)):
            self.scale = np.array([scale, scale, scale], dtype=np.float32)
        else:
            self.scale = np.array(scale, dtype=np.float32)
            
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        
        self.vertices = []
        self.normals = []
        self.faces_by_material = {}  # Organizar caras por material
        self.triangles = []
        
        self._load_obj()
        self._apply_transforms()
        self._create_triangles()
    
    def _load_obj(self):
        """Lee el archivo OBJ y extrae vértices, normales y caras."""
        print(f"\n Cargando OBJ: {self.filepath}")
        
        current_material = "default"
        
        try:
            with open(self.filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Ignorar comentarios y líneas vacías
                    if not line or line.startswith('#'):
                        continue
                    
                    # Vértices (v x y z)
                    if line.startswith('v '):
                        parts = line.split()
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        vertex = np.array([x, y, z], dtype=np.float32)
                        self.vertices.append(vertex)
                    
                    # Normales (vn x y z)
                    elif line.startswith('vn '):
                        parts = line.split()
                        nx, ny, nz = float(parts[1]), float(parts[2]), float(parts[3])
                        normal = normalize(np.array([nx, ny, nz], dtype=np.float32))
                        self.normals.append(normal)
                    
                    # Cambio de material
                    elif line.startswith('usemtl '):
                        material_name = line.split()[1]
                        current_material = material_name
                        if current_material not in self.faces_by_material:
                            self.faces_by_material[current_material] = []
                    
                    # Caras (f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3)
                    elif line.startswith('f '):
                        parts = line.split()
                        indices = []
                        normal_indices = []
                        
                        for part in parts[1:]:
                            values = part.split('/')
                            # Índice de vértice (1-based en OBJ)
                            idx = int(values[0]) - 1
                            indices.append(idx)
                            
                            # Índice de normal (si existe)
                            if len(values) >= 3 and values[2]:
                                nidx = int(values[2]) - 1
                                normal_indices.append(nidx)
                        
                        # Asegurar que hay lista para este material
                        if current_material not in self.faces_by_material:
                            self.faces_by_material[current_material] = []
                        
                        # Triangular si es necesario
                        if len(indices) == 3:
                            self.faces_by_material[current_material].append({
                                'vertices': indices,
                                'normals': normal_indices if normal_indices else None
                            })
                        elif len(indices) == 4:
                            # Dividir quad en 2 triángulos
                            self.faces_by_material[current_material].append({
                                'vertices': [indices[0], indices[1], indices[2]],
                                'normals': [normal_indices[0], normal_indices[1], normal_indices[2]] if normal_indices else None
                            })
                            self.faces_by_material[current_material].append({
                                'vertices': [indices[0], indices[2], indices[3]],
                                'normals': [normal_indices[0], normal_indices[2], normal_indices[3]] if normal_indices else None
                            })
                        elif len(indices) > 4:
                            # Triangular polígonos con más de 4 vértices (fan triangulation)
                            for i in range(1, len(indices) - 1):
                                self.faces_by_material[current_material].append({
                                    'vertices': [indices[0], indices[i], indices[i + 1]],
                                    'normals': [normal_indices[0], normal_indices[i], normal_indices[i + 1]] if normal_indices else None
                                })
            
            total_faces = sum(len(faces) for faces in self.faces_by_material.values())
            
            print(f"  ✓ Vértices: {len(self.vertices)}")
            print(f"  ✓ Normales: {len(self.normals)}")
            print(f"  ✓ Caras totales: {total_faces}")
            print(f"  ✓ Materiales encontrados:")
            for mat_name, faces in self.faces_by_material.items():
                print(f"    • {mat_name}: {len(faces)} caras")
            
        except FileNotFoundError:
            print(f"  ✗ ERROR: Archivo no encontrado: {self.filepath}")
            raise
        except Exception as e:
            print(f"  ✗ ERROR cargando OBJ: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _apply_transforms(self):
        """Aplica escala, rotación y traslación a los vértices."""
        if len(self.vertices) == 0:
            return
        
        # Convertir a array numpy
        vertices = np.array(self.vertices)
        
        # Calcular centro y dimensiones
        min_point = np.min(vertices, axis=0)
        max_point = np.max(vertices, axis=0)
        center = (min_point + max_point) / 2
        dimensions = max_point - min_point
        
        print(f"\n Dimensiones originales: {dimensions}")
        print(f"  Centro original: {center}")
        
        # Centrar el modelo
        vertices -= center
        
        # Aplicar escala
        vertices *= self.scale
        
        # Calcular nuevas dimensiones
        new_dimensions = dimensions * self.scale
        print(f"  Dimensiones escaladas: {new_dimensions}")
        
        # Aplicar rotación (en orden: X, Y, Z)
        rx, ry, rz = np.radians(self.rotation)
        
        # Rotación X
        if abs(rx) > 1e-6:
            Rx = np.array([
                [1, 0, 0],
                [0, np.cos(rx), -np.sin(rx)],
                [0, np.sin(rx), np.cos(rx)]
            ])
            vertices = vertices @ Rx.T
        
        # Rotación Y
        if abs(ry) > 1e-6:
            Ry = np.array([
                [np.cos(ry), 0, np.sin(ry)],
                [0, 1, 0],
                [-np.sin(ry), 0, np.cos(ry)]
            ])
            vertices = vertices @ Ry.T
        
        # Rotación Z
        if abs(rz) > 1e-6:
            Rz = np.array([
                [np.cos(rz), -np.sin(rz), 0],
                [np.sin(rz), np.cos(rz), 0],
                [0, 0, 1]
            ])
            vertices = vertices @ Rz.T
        
        # Aplicar traslación
        vertices += self.position
        
        # Actualizar vértices
        self.vertices = [v for v in vertices]
        
        # Calcular bounding box final
        final_min = np.min(vertices, axis=0)
        final_max = np.max(vertices, axis=0)
        print(f"   Bounding box final:")
        print(f"     Min: {final_min}")
        print(f"     Max: {final_max}")
    
    def _create_triangles(self):
        """Genera objetos Triangle a partir de las caras, usando materiales."""
        print(f"\n  🔨 Generando triángulos...")
        
        for material_name, faces in self.faces_by_material.items():
            # Determinar qué material usar
            if self.materials_dict and material_name in self.materials_dict:
                material = self.materials_dict[material_name]
                print(f"    • {material_name}: usando material personalizado")
            elif self.default_material is not None:
                material = self.default_material
                print(f"    • {material_name}: usando material por defecto")
            else:
                print(f"    ⚠ {material_name}: sin material asignado, saltando...")
                continue
            
            # Crear triángulos para este material
            triangles_count = 0
            for face in faces:
                vertex_indices = face['vertices']
                
                if len(vertex_indices) != 3:
                    continue
                
                v0 = self.vertices[vertex_indices[0]]
                v1 = self.vertices[vertex_indices[1]]
                v2 = self.vertices[vertex_indices[2]]
                
                triangle = Triangle(
                    A=v0.tolist(),
                    B=v1.tolist(),
                    C=v2.tolist(),
                    material=material
                )
                
                self.triangles.append(triangle)
                triangles_count += 1
            
            print(f"      → {triangles_count} triángulos generados")
        
        print(f"  ✓ Total de triángulos: {len(self.triangles)}")
    
    def get_triangles(self):
        """Retorna la lista de triángulos para agregar a la escena."""
        return self.triangles


def load_obj(filepath, material=None, materials_dict=None, 
             scale=1.0, position=(0, 0, 0), rotation=(0, 0, 0)):
    """
    Función helper para cargar un OBJ.
    
    Args:
        filepath: Ruta al archivo .obj
        material: Material por defecto
        materials_dict: Diccionario de materiales por nombre
                       Ejemplo: {'Bark': mat_corteza, 'Tree': mat_follaje}
        scale: Escala (float o tuple de 3 valores)
        position: Posición (x, y, z)
        rotation: Rotación (rx, ry, rz) en grados
    
    Returns:
        Lista de triángulos
    
    Ejemplos:
        # Uso básico con un solo material
        triangles = load_obj('model.obj', material=mat_default, scale=2.0)
        
        # Uso con múltiples materiales
        triangles = load_obj(
            'tree.obj',
            materials_dict={
                'Bark': mat_brown,
                'Tree': mat_green
            },
            scale=2.0,
            position=(0, 0, 0)
        )
    """
    model = OBJModel(filepath, material, materials_dict, scale, position, rotation)
    return model.get_triangles()