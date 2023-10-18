from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Useful python libraries'
LONG_DESCRIPTION = 'Useful python libraries'

setup(
        name="myLibs", 
        version=VERSION,
        author="Carlos Finocchiaro",
        author_email="<carlosfinocchiaro@hotmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],        
        keywords=['python', 'myLibs'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)