from setuptools import setup, find_packages

# Leer documentos del "README.md"
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="MiPaquetito",
    version="0.0.1",
    packages= find_packages(),
    install_requires=[],
    author="Epsaind dev",
    description= "Una Biblioteca para poder ver mi pequeña Python",
    long_description = long_description,
    long_description_content_type= "text/markdown",
    url="https://epsaind.dev",

)

