#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    "numpy",
    "matplotlib>=3.3",
    "sympy",
    "jupyter",
    "pyshtools>=4.9",
    "cmcrameri",
]

setup(
    name="Displacement_strain_planet",
    version="0.5.0",
    description="Planetary crustal thickness, displacement, "
    + "stress and strain calculations in spherical harmonics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AB-Ares/Displacement_strain_planet",
    author="Adrien Broquet",
    author_email="adrienbroquet@arizona.edu",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering",
    ],
    keywords=[
        "stress",
        "strain",
        "flexure",
        "elastic thickness",
        "crust",
        "gravity",
        "geophysics",
        "Mars",
        "planetary sciences",
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=install_requires,
    python_requires=">=3.7",
)
