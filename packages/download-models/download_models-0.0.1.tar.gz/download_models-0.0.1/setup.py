from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys

__version__ = "0.0.1"

with open("requirements.txt") as f:
    require_packages = [line[:-1] if line[-1] == "\n" else line for line in f]

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="download_models",
    version=__version__,
    author='Tangesion',
    author_email='tangesion@163.com',
    packages=find_packages(),
    install_requires=require_packages,
    #url="https://github.com/",
    description="Download models from hugging face",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'tdownload = src.download:main'
        ]
    }
)