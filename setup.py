import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_steam_queries",
    install_requires=['steam'],
    version="1.0.4",
    author="Giannis Spentzas",
    author_email="gspentzas1991@gmail.com",
    description="A python module that allows you to easily run Steam Master Server Query Protocol queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gspentzas1991/Simple-Steam-Queries",
    packages=find_packages(include=['simple_steam_queries', 'simple_steam_queries.*']),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)