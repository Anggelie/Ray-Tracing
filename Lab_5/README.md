# Laboratorio 5 – RayTracer Simple (Murciélago)

## Integrante
- Anggelie Velásquez – 221181

---

## Objetivos
- Preparar el ambiente de desarrollo para un RayTracer simple.  
- Dibujar esferas con sus respectivos materiales.  
- Implementar un modelo de iluminación **Phong**.  
- Renderizar una figura compuesta por varias esferas de diferentes materiales.  

---

## Requerimientos cumplidos
- Código fuente capaz de **renderizar esferas** por medio de un algoritmo de intersección rayo–esfera.  
- Uso de **modelo de iluminación Phong** (componentes Ambiente + Difusa + Especular).  
- Figura compuesta por múltiples esferas con diferentes materiales: **Murciélago en una rama**.  
- La figura aparece **centrada y completamente visible** en la ventana.  

---

## Archivos principales
- `Rasterizer2025.py` → Programa principal, define escena y render.  
- `sphere.py` → Clase `Sphere` con intersección rayo–esfera.  
- `material.py` → Clase `Material` con propiedades difusas, especulares y shininess.  
- `light.py` → Luces direccionales y ambiente.  
- `shading.py` → Implementación del modelo de iluminación Phong.  
- `vec.py` → Utilidades matemáticas (vectores).  
- `camera.py` → Manejo de cámara y rayos.  
- `gl.py` → Renderizador base.  
- `image_saver.py` → Guardado de imágenes.  

---

## Ejecución
1. Instalar dependencias:
   ```bash
   pip install pygame numpy
2. Ejecutar programa:
   ```bash
   python Rasterizer2025.py
   ```