#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='stockmarketsignals-gateway',
    version='0.0.1',
    description='Gateway for Stock Market Signals',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "marshmallow==2.9.1",
        "nameko==2.6.0",
    ],
    extras_require={
        'dev': [
            'pytest==3.1.1',
            'coverage==4.4.1',
            'flake8==3.3.0'
        ],
    },
    zip_safe=True
)
