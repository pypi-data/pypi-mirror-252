from setuptools import setup, find_packages


"""
:authors: Krislav
:copyright: (c) 2023 Krislav
"""

version = '0.2.1'

long_description = '''Python module for my own use'''

setup(
    name='KrislavLibraryPy',
    version=version,

    author='Krislav',
    author_email='kirill.sokolyansky@gmail.com',

    description='Python module for my own use',
    long_description=long_description,

    packages=find_packages(),
    install_requires=[],
)
