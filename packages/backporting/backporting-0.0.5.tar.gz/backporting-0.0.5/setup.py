#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="backporting",
    version="0.0.5",
    description="A Python client for backporting.",
    license="MIT",
    author="LY",
    author_email="",
    url="https://github.com/levon2111/backporting.git",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
    ],
    keywords="Backporting",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=True,
    py_modules=["backporting"],

)