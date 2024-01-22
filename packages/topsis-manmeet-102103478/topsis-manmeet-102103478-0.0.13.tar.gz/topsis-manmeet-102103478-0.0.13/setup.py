from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.13'
DESCRIPTION = 'It finds the topsis and rank of the input file'
LONG_DESCRIPTION = 'It finds the topsis and rank of the input file'

# Setting up
setup(
    name="topsis-manmeet-102103478",
    version=VERSION,
    author="Manmeet Sidhu",
    author_email="msidhu_be21@thapar.edu",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)