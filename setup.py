#! coding: utf-8
from setuptools import setup, find_packages

setup(
    name='games_entrainment',
    version='0.1.0',
    author="Juan Manuel Pérez",
    author_email="jmperez.85@gmail.com",
    url="https://github.com/geekazoid/tesis",
    packages=find_packages('games_entrainment'),
    install_requires=[
        "configparser == 3.5.0",
        "dill == 0.2.2",
        "fire == 0.1.1",
        "numpy == 1.10.1",
        "pandas == 0.17.1",
        "scipy==0.16.1",
        "sympy==0.7.5",
        "pydub==0.20.0",
    ],
)
