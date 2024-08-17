#!/usr/bin/env python3

from .courses import courses

def total_duration():

    print(f"\n[+] La suma de las horas totales de los cursos es de {sum(course.duration for course in courses)}\n")
