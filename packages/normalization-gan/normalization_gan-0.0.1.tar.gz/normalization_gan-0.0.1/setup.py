import os

from setuptools import find_packages, setup

VERSION = "0.0.1"
# DESCRIPTION = "gpt 4 normalization library"
# LONG_DESCRIPTION = "My first Python package with a slightly longer description"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="normalization_gan",
    version=VERSION,
    author="Aruj Deshwal",
    author_email="aruj@gan.studio",
    description=open("README.md").read(),
    # long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["openai"],
    keywords=["python"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
