# Shading mejorado con Phong

import numpy as np

def phong_shade(point, normal, view_dir, material, lights, ambient=0.1):
    """
    Implementación del modelo de iluminación Phong
    
    Args:
        point: Punto de intersección
        normal: Normal en el punto (debe estar normalizada)
        view_dir: Dirección hacia la cámara (debe estar normalizada)
        material: Material del objeto
        lights: Lista de luces
        ambient: Componente de luz ambiente
    
    Returns:
        Color RGB resultante
    """
    # Asegurar que los vectores están normalizados
    normal = np.array(normal) / np.linalg.norm(normal)
    view_dir = np.array(view_dir) / np.linalg.norm(view_dir)
    
    # Componente ambiente
    color = np.array(material.color) * ambient
    
    # Procesar cada luz
    for light in lights:
        # Dirección de la luz (normalizada)
        light_dir = -np.array(light.direction)  # Negativo porque direction apunta desde la luz
        light_dir = light_dir / np.linalg.norm(light_dir)
        
        # Componente difusa (Lambert)
        diffuse_intensity = max(0.0, np.dot(normal, light_dir))
        diffuse_color = (np.array(material.color) * 
                        np.array(light.color) * 
                        diffuse_intensity * 
                        light.intensity)
        
        # Componente especular (Phong)
        if diffuse_intensity > 0:  # Solo si hay contribución difusa
            # Vector de reflexión
            reflect_dir = 2 * normal * np.dot(normal, light_dir) - light_dir
            reflect_dir = reflect_dir / np.linalg.norm(reflect_dir)
            
            # Intensidad especular
            spec_intensity = max(0.0, np.dot(view_dir, reflect_dir))
            spec_intensity = pow(spec_intensity, material.shininess)
            
            specular_color = (np.array(light.color) * 
                            material.specular * 
                            spec_intensity * 
                            light.intensity)
        else:
            specular_color = np.array([0.0, 0.0, 0.0])
        
        # Sumar contribuciones
        color += diffuse_color + specular_color
    
    # Clamp al rango [0,1]
    return np.clip(color, 0.0, 1.0)