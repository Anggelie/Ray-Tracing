# Lab 06 – Opaque, Reflective & Refractive Materials

## Objetivos
- Preparar el ambiente de desarrollo para un modelo de iluminación simple.
- Dibujar esferas con materiales opacos, reflectivos y transparentes.
- Utilizar un Environment Map distinto al visto en clase para los reflejos y refracciones.
- Visualizar el resultado en tiempo real con Pygame.

---

## Requerimientos cumplidos
- Código fuente capaz de renderizar esferas por medio de un algoritmo de intersección rayo–esfera.
- Uso de modelo de iluminación **Phong** (componentes Ambiente + Difusa + Especular).
- Implementación de materiales:
  - **Opacos**
  - **Reflectivos**  
  - **Transparentes/Refractivos** 
- Escena con **6 esferas visibles** 
- Fondo cargado desde **Environment Map** 
- La escena aparece centrada y completamente visible en la ventana de Pygame.

---

## Archivos principales
- `Raytracer2025.py` → Programa principal, define escena y ejecuta el render.
- `gl.py` → Renderer base con ray casting, manejo de cámara y environment map.
- `material.py` → Clase `Material` con soporte para opaco, reflectivo y transparente (refracción).
- `lights.py` → Luces direccionales y ambiente (Phong).
- `refractionFunctions.py` → Cálculo de refracción (Snell) y Fresnel.
- `figures.py` → Clase `Sphere` con intersección rayo–esfera.
- `MathLib.py` → Utilidades matemáticas (vectores, reflect).
- `BMPTexture.py` → Carga de texturas BMP (24 bits).
- `Textures/` → Carpeta con imágenes BMP usadas (incluye `bloem_field_sunrise_24.bmp` como environment map).

---
##  Ejecución

1. Instalar dependencias:
   ```bash
   pip install pygame numpy
2. Ejecutar el programa:
   ```bash
    python Raytracer2025.py
3. Se abrirá una ventana de Pygame mostrando la escena:
* 2 esferas opacas
* 2 esferas reflectivas
* 2 esferas transparentes
* Fondo con Environment Map realista

4. Para cerrar, presionar ESC o el botón de cerrar ventana.
