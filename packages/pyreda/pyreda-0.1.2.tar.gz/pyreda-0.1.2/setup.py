from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyreda',
    version='0.1.2',
    description='A Python Library for Building the Genetic Algorithm.',
    author='Reda Ghanem',
    author_email='reda.ghanem66@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Important for correct formatting on PyPI
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pickle-mixin',   # In case you are using the pickle module
        'joblib',
        'pandas',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
