from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Useful Functions'
LONG_DESCRIPTION = 'Useful functions for various applications'

# Setting up
setup(
    name="useful_funcs",
    version=VERSION,
    author="SuryaSudh",
    author_email="<suryasudhakar7@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['datetime', 'numpy'],
    keywords=['python', 'useful', 'useful functions', 'unit conversion', 'date conversion', 'calendar functions'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],

)