from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'My First Package'
LONG_DESCRIPTION = '''

Area Calculator

# first_package

`first_package` is a Python package that provides a set of functions to calculate the areas of geometric shapes. It includes a module named `Area_Fig.py` containing three functions:

- `square_area(side_length)`: Calculates the area of a square given the length of its side.
- `rectangle_area(length, width)`: Calculates the area of a rectangle given its length and width.
- `circle_area(radius)`: Calculates the area of a circle given its radius.

## Installation

Install `first_package` using pip: pip install first_package

## Usage

from first_package.Area_Fig import square_area, rectangle_area, circle_area

### Calculate the area of a square
print(square_area(5))

### Calculate the area of a rectangle
print(rectangle_area(4, 6))

### Calculate the area of a circle
print(circle_area(3))
'''

# Setting up
setup(
    name="AreaOfFig24test",
    version=VERSION,
    author="Himanshu Bansal",
    author_email="himu90505@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['area of figs', 'area', 'himanshu'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)