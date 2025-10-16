# Proyecto 2 - Ray Tracer con Modelo OBJ

**Gráficas por Computadora**  
**Universidad del Valle de Guatemala**

---

## Descripción

Implementación de un ray tracer completo en Python que renderiza escenas 3D con múltiples figuras geométricas, materiales avanzados, iluminación realista y soporte para modelos OBJ.

---

##  Figuras Geométricas Implementadas

### Básicas:
- **Sphere** - Esferas con iluminación Phong
- **Plane** - Planos infinitos
- **Cube** - Cubos axis-aligned (AABB)

### Avanzadas:
- **Cylinder** - Cilindros con tapas y UV mapping
- **Torus** - Toros (superficie cuártica)
- **Ellipsoid** - Elipsoides (esferas escaladas)
- **Triangle** - Triángulos (usado por OBJ loader)

---

##  Sistema de Materiales

### Propiedades:
- **Diffuse (kd)** - Componente difusa
- **Specular (ks)** - Componente especular
- **Shininess** - Intensidad del brillo especular
- **Texture** - Soporte para texturas (checker, imagen)

### Tipos de texturas:
- **CheckerTexture** - Patrón de tablero de ajedrez
- **ImageTexture** - Texturas desde archivos de imagen
- **EnvMap** - Environment mapping esférico

---

## Sistema de Iluminación

### Tipos de luces:
- **AmbientLight** - Iluminación ambiental uniforme
- **DirectionalLight** - Luz direccional (sol)
- **PointLight** - Luz puntual con atenuación

### Efectos:
- Sombras duras (shadow rays)
- Reflexiones (ray tracing recursivo)
- Modelo de iluminación Blinn-Phong

---

##  Carga de Modelos OBJ

### Características del loader:
-  Soporte multi-material
-  Carga de vértices y normales
- Triangulación automática de quads y polígonos
- Transformaciones (escala, rotación, traslación)
-  Centrado automático del modelo

---

##  Instalación

### Requisitos:
- Python 3.8+
- NumPy
- Pygame

### Instalación de dependencias:
```bash
pip install numpy pygame
```

---

##  Ejecución

### Render principal:
```bash
python Raytracer_Proyecto2.py
```

### Configuración de resolución:
Edita las líneas 252-253 en `Raytracer_Proyecto2.py`:

```python
# Resolución baja (rápido - ~30 min)
RES_PREVIEW = (240, 300)

# Resolución media (~5 horas)
RES_PREVIEW = (480, 600)

# Resolución alta (~8-12 horas)
RES_FINAL = (960, 1200)
```

---

## Estructura del Proyecto

```
Proyecto_2/
├── Raytracer_Proyecto2.py          # Script principal
├── Lowpoly_tree_sample.obj         # Modelo 3D del árbol
│
├── Textures/                       # Motor de ray tracing
│   ├── gl.py                       # Raytracer core
│   ├── figures.py                  # Figuras geométricas
│   ├── material.py                 # Sistema de materiales
│   ├── lights.py                   # Sistema de iluminación
│   ├── obj_loader.py               # Cargador de OBJ
│   ├── envmap.py                   # Environment mapping
│   ├── checker.py                  # Textura checker
│   ├── texture.py                  # Texturas de imagen
│   ├── intercept.py                # Intersecciones
│   ├── MathLib.py                  # Matemáticas (vectores)
│   └── env_sky.bmp                 # Textura de cielo
│
├── BMP/
│   └── BMP_Writer.py               # Guardado de imágenes
│
└── renders/                        # Imágenes generadas
    ├── proyecto2_COMPLETO_preview.bmp
    └── proyecto2_COMPLETO_FINAL.bmp
```

---


### Iluminación:
- 1 luz ambiental
- 1 luz puntual principal
- 2 luces direccionales (fill lights)

---

##  Optimizaciones

### Para renders rápidos:
1. **Reducir resolución**: Usa 240x300 para pruebas
2. **Reducir max_depth**: Cambia a 2 en lugar de 3-4
3. **Menos rebotes de luz**: Menos cálculos de reflexión

### Para calidad máxima:
1. **Alta resolución**: 960x1200 o superior
2. **max_depth = 4**: Más reflexiones
3. **Anti-aliasing**: Múltiples rays por pixel (no implementado)

---

##  Solución de Problemas

### El render toma demasiado tiempo:
- Reduce la resolución en el código
- Reduce `max_depth` en `build_final_scene()`
- El modelo OBJ tiene muchos triángulos (312), considera usar uno más simple para las pruebas si no se tardara mucho tiempo

---

## Referencias

### Algoritmos implementados:
- **Ray-Sphere intersection** - Solución analítica
- **Ray-Plane intersection** - Producto punto
- **Ray-Triangle intersection** - Algoritmo de Möller-Trumbore
- **Ray-Torus intersection** - Solución de cuártica con numpy.roots
- **Blinn-Phong shading** - Modelo de iluminación
- **Environment mapping** - Proyección equirectangular

### Recursos:
- Scratchapixel (ray tracing fundamentals)
- Real-Time Rendering (iluminación y sombreado)
- OBJ Format Specification (Wavefront)

---

## Autor

**Anggelie Velásquez**  
Universidad del Valle de Guatemala  
Gráficas por Computadora - 2025
