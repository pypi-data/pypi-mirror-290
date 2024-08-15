#!/usr/bin/env python3

from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    longDescription = fh.read()

setup(
    name="THack4u",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Treizer",
    description="Una biblioteca para consultar cursos de hack4u.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://hack4u.io"
)
