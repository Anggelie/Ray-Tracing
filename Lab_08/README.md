# Lab 8: Ray-Intersect Algorithm, New Shapes  

## Objetivo
El objetivo de este laboratorio fue **investigar e implementar algoritmos de intersección de rayos (Ray-Intersect Algorithm)** para nuevas figuras geométricas dentro de un **RayTracer simple** que hemos estado desarrollando en clase.  

En particular, se trabajó con:  
- **Cilindro**  
- **Toroide (dona)**  

Cada figura fue implementada desde cero en el archivo `figures.py`, integrándose al motor base y probada en diferentes posiciones, escalas y con distintos materiales (difuso, reflectivo y transparente).  

---

## Archivos principales del proyecto

- `Raytracer_Lab08.py` → versión base del laboratorio con render inicial.  
- `Raytracer_Lab08_room_centered_plus.py` → versión final con mejoras de composición (cuarto completo, piso ajedrezado y figuras bien distribuidas).  
- `figures.py` → incluye todas las primitivas geométricas y **nuevas figuras** (cilindro, toroide, elipsoide, etc.).  
- `config.py` → centraliza parámetros de cámara, luces y dimensiones de render.  
- `gl.py` → motor del Raytracer (buffer, cámara y funciones base).  
- `material.py` → definición de materiales (difuso, reflectivo, transparente).  
- `lights.py` → implementación de luces (ambiental, puntual y direccional).  
- `MathLib.py` → utilidades matemáticas como normalización de vectores.  
- `BMP_Writer.py` → exportación de resultados en formato `.bmp`.  

---

## Mejoras realizadas
- **Figures.py**
  - Se implementó **Cylinder** con intersección en tapas y cuerpo.  
  - Se implementó **Torus** usando solución polinómica de cuarto grado.  
  - Se mejoró la normalización y estabilidad numérica.  
  - Se añadieron otras primitivas adicionales como `Ellipsoid` y `Cube`.  

- **Config.py**
  - Se parametrizó resolución (rápida 128x128 o final 512x512).  
  - Configuración de cámara y luces desde un solo archivo.  

- **Raytracer**
  - Se agregaron métodos de render mejorado.  
  - Se construyó un cuarto con **paredes, piso reflectivo y techo** para tener un entorno más realista.  
  - Se añadieron **materiales pastel + metálicos y transparentes**.  
  - Se incorporó un **piso ajedrezado reflectivo**.  

---

### Versión mejorada
- Cuarto cerrado con **paredes, techo y piso reflectivo**.  
- Cámara centrada tipo interior, para simular estar dentro de una habitación.  
- Figuras distribuidas simétricamente (3 cilindros + 3 toros) con materiales distintos:
  - Difuso (mate, pastel).  
  - Reflectivo (metal).  
  - Transparente (vidrio).  

Los resultados se encuentran en la carpeta `renders/`:  
- `Lab08_render.bmp`  
- `Lab08_render_frontal.bmp`  
- `Lab08_render_mejorado.bmp`  
- `Lab08_room_plus.bmp`  

---

## Iluminación
Se emplearon diferentes configuraciones de luces:  
- **Luz ambiental** para iluminar el cuarto.  
- **Luz puntual en el techo** simulando un plafón.  
- **Luces direccionales** para rellenar sombras y dar más realismo.  

---

## Pruebas realizadas
1. Render con resolución baja (128x128 y 800x600) → validación rápida de intersecciones.  
2. Render con materiales distintos → comprobación de comportamiento (opaco, reflectivo y transparente).  
3. Render en cuarto cerrado → validación de proporciones de cámara y reflexiones en el piso.  
4. Exportación de BMP → pruebas de guardado automático y apertura de imágenes.  

---

##  Conclusiones
- Se logró implementar correctamente **dos nuevas figuras geométricas (Cilindro y Toroide)** y extender el RayTracer.  
- La inclusión de materiales variados permitió validar la robustez de los algoritmos.  
- Con las mejoras visuales (piso ajedrezado y cuarto cerrado), se obtuvieron renders más realistas y comparables a los de los compañeros.  
- Este laboratorio fortalece el entendimiento de cómo los **ray-figura intersections** son la base para cualquier motor de render moderno.  

## Ejecución
Para correr el laboratorio:

```bash
cd Lab_08
 python Raytracer_Lab08.py