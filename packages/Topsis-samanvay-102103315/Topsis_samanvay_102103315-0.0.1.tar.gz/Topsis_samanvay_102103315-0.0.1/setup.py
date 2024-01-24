from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'topsis package for decision making'
with open("README.md", "r") as fh:
    long_description = fh.read()


# Setting up
setup(
    name="Topsis_samanvay_102103315",
    version=VERSION,
    author="samanvay",
    author_email="=ssrivastava_be21@thapar.edu",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=find_packages(),
    install_requires=['logging', 'numpy', 'pandas'],
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