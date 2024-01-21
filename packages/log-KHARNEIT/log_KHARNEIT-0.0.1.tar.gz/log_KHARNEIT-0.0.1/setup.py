from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'CustomLog'
LONG_DESCRIPTION = 'Custom logging class for console and/or file output'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="log_KHARNEIT",
    version=VERSION,
    author="Karsten Harneit",
    author_email="<karsten@harne.it>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'logging'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)