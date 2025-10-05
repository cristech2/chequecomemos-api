---
description: 'Convenciones y directrices de codificación de Python para mantener la calidad y la coherencia en el proyecto.'
applyTo: '**/*.py'
---

# Convenciones de Codificación en Python

## Instrucciones de Python

- Escribe comentarios claros y concisos para cada función.
- Asegúrate de que las funciones tengan nombres descriptivos e incluyan anotaciones de tipo.
- Proporciona docstrings siguiendo las convenciones de PEP 257.
- Utiliza el módulo `typing` para anotaciones de tipo (por ejemplo, `List[str]`, `Dict[str, int]`).
- Divide funciones complejas en funciones más pequeñas y manejables.

## Instrucciones Generales

- Siempre prioriza la legibilidad y claridad.
- Para el código relacionado con algoritmos, incluye explicaciones del enfoque utilizado.
- Escribe código con buenas prácticas de mantenibilidad, incluyendo comentarios sobre por qué se tomaron ciertas decisiones de diseño.
- Maneja casos límite y escribe un manejo de excepciones claro.
- Para bibliotecas o dependencias externas, menciona su uso y propósito en los comentarios.
- Utiliza convenciones de nomenclatura consistentes y sigue las mejores prácticas específicas del lenguaje.
- Escribe código conciso, eficiente e idiomático que también sea fácilmente comprensible.

## Estilo de Código y Formateo

- Sigue la guía de estilo **PEP 8** para Python.
- Mantén la indentación adecuada (usa 4 espacios para cada nivel de indentación).
- Asegúrate de que las líneas no excedan los 79 caracteres.
- Coloca los docstrings de funciones y clases inmediatamente después de la palabra clave `def` o `class`.
- Usa comillas triples dobles (`"""`) para docstrings.
- Usa comillas simples (`'`) o dobles (`"`) de manera consistente para cadenas.
- Evita líneas en blanco innecesarias.
- Utiliza líneas en blanco para separar funciones, clases y bloques de código donde sea apropiado.

## Casos Límite y Pruebas

- Siempre incluye casos de prueba para los caminos críticos de la aplicación.
- Ten en cuenta casos límite comunes como entradas vacías, tipos de datos no válidos y conjuntos de datos grandes.
- Incluye comentarios para los casos límite y el comportamiento esperado en esos casos.
- Escribe pruebas unitarias para las funciones y documéntalas con docstrings que expliquen los casos de prueba.

## Ejemplo de Documentación Adecuada

```python
def calculate_area(radius: float) -> float:
    """
    Calcula el área de un círculo dado el radio.

    Parameters:
    radius (float): El radio del círculo.

    Returns:
    float: El área del círculo, calculada como π * radius^2.
    """
    import math
    return math.pi * radius ** 2
```
