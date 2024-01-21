from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.1'
DESCRIPTION = 'Creates a randomly generated password using the "pytoken.pytoken()" function.'
setup(
    name="pytoken",
    version=VERSION,
    author="Flavko",
    author_email="<flavio013568@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['random', 'string'],
    keywords=['python', 'token', 'generator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
