from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Quickly retrieve the current IPv4 address of your machine.'
LONG_DESCRIPTION = 'NetLocator is a Python utility designed to fetch the current IPv4 address of your machine with ease.'

# Setting up
setup(
    name="netLocator",
    version=VERSION,
    author="Yasiru Perera",
    author_email="yasiruperera681@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['subprocess'],
    keywords=['python', 'network', 'IP address', 'IPv4', 'network utilities'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ]
)
