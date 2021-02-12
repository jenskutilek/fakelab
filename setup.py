#! /usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fakelab",
    version="0.1.0",
    description="Fake FontLab for automated tests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jens Kutilek",
    url="https://github.com/jenskutilek/fakelab",
    packages=[
        "FL",
    ],
    package_dir={"": "lib"},
    scripts=[
    ],
    install_requires=[
        "pytest",
    ],
    dependency_links=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
