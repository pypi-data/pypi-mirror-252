# setup.py
from setuptools import setup, find_packages

setup(
    name='topsis-shrey-102103354',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'topsis = topsis.topsis:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
