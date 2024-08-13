from setuptools import setup, find_packages

VERSION = '1.1.1'
DESCRIPTION = 'Quick and easy python functions for all purposes.'
LONG_DESCRIPTION = 'A quick and easy way to replace big chunks of code with a few functions.'

# Setting up
setup(
    name="quick_access",
    version=VERSION,
    author='MITdude',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'easy', 'python quick', 'quick access'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)