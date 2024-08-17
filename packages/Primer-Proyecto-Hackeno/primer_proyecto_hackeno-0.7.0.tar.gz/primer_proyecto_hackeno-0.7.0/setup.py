#!/usr/bin/env python3

from setuptools import setup, find_packages

# Leer el contenido del archivo README creado anteriormente

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Primer_Proyecto_Hackeno",
    version="0.7.0",
    packages=find_packages(),
    install_requires=[],
    author="Marcelo Vázquez",
    description="Una biblioteca para consultar los distintos cursos de la academia Hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
