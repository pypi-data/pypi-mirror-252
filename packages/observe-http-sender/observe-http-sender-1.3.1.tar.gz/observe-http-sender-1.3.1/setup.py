#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

with open("requirements.txt") as requirement_file:
    requirements = requirement_file.read().split()

# Parse version number from __init__.py:
with open('__init__.py') as init_file:
    info = {}
    for line in init_file:
        if line.startswith('version'):
            exec(line, info)
            break

# Fetch README.md for long description       
def readme():
    with open('./README.md') as f:
        return f.read()

# Setup for package
setup(name='observe-http-sender',
    python_requires='>=3.7',
    install_requires=requirements,
    version=info['version'],
    description='Python class to send events to an Observe Inc Datastream.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Observe Inc',
    packages=find_packages(),
    url='https://github.com/observeinc/observe-http-sender-python',
    download_url='https://github.com/observeinc/observe-http-sender-python/archive/refs/heads/main.zip',
    py_modules=['observe_http_sender'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Framework :: AsyncIO',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
     )
