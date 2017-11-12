#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='stockmarketsignals-signals',
    version='0.0.1',
    description='Signals API Service',
    author='joaogabriellima',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['signals'],
    install_requires=[
        "marshmallow==2.9.1",
        "nameko==2.6.0",
        "redis==2.10.5",
        "xmltodict==0.11.0",
        "bs4==0.0.1"
    ],
    extras_require={
        'dev': [
            'pytest==3.1.1',
            'coverage==4.4.1',
            'flake8==3.3.0'
        ]
    },
    zip_safe=True,
)
