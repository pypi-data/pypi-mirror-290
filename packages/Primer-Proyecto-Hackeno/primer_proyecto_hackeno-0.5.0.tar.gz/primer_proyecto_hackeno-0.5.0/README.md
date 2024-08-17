# Hack4u Academy Courses Library

Una biblioteca Python para consultar los cursos de la academia Hack4u.

## Cursos disponibles:

- Introducción a Linux [15 horas]
- Personalización de Linux [3 horas]
- Introducción al Hacking [53 horas]

## Instalación

Instala el paquete utilizando `pip3`:

```python3
pip3 intall Primer_Proyecto_Hackeño
```

# Uso básico

## Listar todos los cursos

```python
from Primer_Proyecto_Hackeño import list_courses

for course in list_courses():
    print(course)
```

## Obtener un curso por nombre

```python
from Primer_Proyecto_Hackeño import get_course_by_name

course = get_course_by_name("Introducción a Linux")
print(course)
```

## Calcular la duración total de los cursos

```python3
from Primer_Proyecto_Hackeño.utils import total_duration

print(f"Duración total: {total_duration()} horas")
```
