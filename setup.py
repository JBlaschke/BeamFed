#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools



with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="beamfed",
    version="0.0.1",
    author="Johannes Blaschke",
    author_email="johannes@blaschke.science",
    description="A DataFed wrapper for beamline data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBlaschke/BeamFed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "datafed"
    ],
)
