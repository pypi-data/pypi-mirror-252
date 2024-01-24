from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'topsis package for decision making'
with open("README.md", "r") as fh:
    long_description = fh.read()


# Setting up
setup(
    name="topsis_anadya_102103021",
    version=VERSION,
    author="Anadya Sahai",
    author_email="=anadya.sahai@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=['pandas','numpy'],
    keywords=['python', 'topsis', 'mcdm', 'data science'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)