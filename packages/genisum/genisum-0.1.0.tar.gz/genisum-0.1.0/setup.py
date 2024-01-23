from setuptools import setup, find_packages

setup(
    name='genisum',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # none
    ],
    author='Arefin Genius',
    description='A simple library for summation of a given list',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)