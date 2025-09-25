# Lab 7 – Planes, Disks, Triangles & Cubes (Ray Tracer)

Render de una escena con **planos, discos, triángulos y cubos** usando un algoritmo de **Ray–Intersection**.  
El objetivo es montar un cuarto tridimensional y colocar en él diferentes figuras con materiales y luces.

## Objetivos
- Implementar y renderizar intersecciones de **Plane**, **Disk**, **Triangle** y **Cube (AABB)**.
- Crear una escena tipo “cuarto” con:
  - 5 planos (piso, techo, fondo, izquierda, derecha)
  - 2 cubos
  - 1 triángulo
  - 1 disco
- Definir materiales y configurar un sistema de iluminación.

---

## Cómo ejecutar

1. Instalar dependencias necesarias:
   ```bash
   pip install numpy
2. Ejecutar desde la carpeta Lab_07/:
   ```bash
   python Raytracer_Lab07.py

3. El resultado se guarda en:
   ```bash
   renders/Lab07_Final.bmp
   
## Primitivas implementadas
- Plane(position, normal, material)
Intersección:
   ```bash
   t = ((P0 - O) · n) / (d · n)

- Disk(position, normal, radius, material)
  Intersección con el plano + verificación de radio.
- Triangle(A, B, C, material)
 Normal:
   ```bash
   n = normalize((B - A) × (C - A))
Se valida si el punto está dentro del triángulo.

- Cube(min, max, material) (Axis-Aligned Bounding Box – AABB)
  Se intersecta el rayo con los planos x/y/z y se verifica si los rangos coinciden.

## Iluminación y materiales
- Luces soportadas:
  - AmbientLight (color, intensidad)

  - DirectionalLight (dirección, color, intensidad)

  - PointLight (posición, color, intensidad)

- Material:
  - color (RGB en rango 0–1)

  - kd (difuso)

  - ks (especular)

  - shininess (brillo especular)

  - mtype = MAT_DIFFUSE o MAT_REFLECTIVE

## Camara y render
- Parámetros:

  - eye, target, up, fov

- Calidad configurable:

  - samples_per_pixel (anti-aliasing)

  - enable_ao, ao_samples, ao_distance (Ambient Occlusion)

  - max_depth (rebotes para reflexión)