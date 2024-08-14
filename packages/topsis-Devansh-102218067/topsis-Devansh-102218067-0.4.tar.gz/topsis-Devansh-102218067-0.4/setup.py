# setup for topsis

from setuptools import setup, find_packages

setup(
    name='topsis-Devansh-102218067',
    version='0.4',
    description='A Python package for TOPSIS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Devansh Arya',
    author_email='Dv30arya@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Topsis=topsis.topsis:main',
        ],
    },
    install_requires=[
        'numpy',
        'pandas',
        'argparse',
        'scipy',
    ],
)
