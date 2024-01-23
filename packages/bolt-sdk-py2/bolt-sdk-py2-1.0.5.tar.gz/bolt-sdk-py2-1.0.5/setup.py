#!/usr/bin/env python
import setuptools
from setuptools import setup
import io

requires = ['boto3', 'botocore']
python_requires = '>=2.7'

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='bolt-sdk-py2',
    packages=setuptools.find_packages(),
    version='1.0.5',
    description='Bolt Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Project N',
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=python_requires,
    url="https://github.com/projectn-oss/projectn-bolt-python2",
)
