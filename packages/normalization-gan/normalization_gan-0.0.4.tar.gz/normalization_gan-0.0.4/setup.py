import os

from setuptools import find_packages, setup

VERSION = "0.0.4"
DESCRIPTION = "Normalization for TTS Input"
try:
    import pypandoc

    LONG_DESCRIPTION = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError):
    LONG_DESCRIPTION = open("README.md").read()


setup(
    name="normalization_gan",
    version=VERSION,
    author="Aruj Deshwal",
    author_email="aruj@gan.studio",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
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
