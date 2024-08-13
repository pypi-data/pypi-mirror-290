# setup.py is a Python script that defines the metadata for the package, such as its name, version, and dependencies. It also contains a call to setuptools.setup() to create the package distribution.

from setuptools import setup, find_packages

setup(
    name="regexable",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Orion Forowycz",
    description="A more readable alternative to regular expressions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Orion-F/regexable",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
