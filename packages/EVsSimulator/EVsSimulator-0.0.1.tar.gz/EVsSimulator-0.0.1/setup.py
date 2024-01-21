# This is a setup file for the package

from setuptools import find_packages
from setuptools import setup


with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='EVsSimulator',
    version='0.0.1',
    description='A realistic V2X environment using gym',
    author='Stavros Orfanoudakis',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords='gym, Reinforcement Learning, V2X, EVs, EVsSimulator, Electric Vehicles, Electric Vehicle Simulator',
    package_dir = {"": "EVsSimulator"},
    packages = find_packages(where="EVsSimulator"),
    python_requires = ">=3.6",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
                      