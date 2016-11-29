#!/usr/bin/env python
"""Defines the setup instructions for ec2-meta-env"""
import os

from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ec2-meta-env',
    version='0.1.1',
    description='A simple package to manifest EC2 instance metadata as environment variables.',
    long_description=read('README.rst'),
    author='Tobias McNulty',
    author_email='tobias.mcnulty@gmail.com',
    url='https://github.com/tobiasmcnulty/ec2-meta-env',
    license="MIT",
    py_modules=['ec2_meta_env'],
    entry_points={
        'console_scripts': ['ec2-meta-env=ec2_meta_env:main'],
    },
    requires=[],
    install_requires=['requests'],
    keywords='Python, Python3',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
