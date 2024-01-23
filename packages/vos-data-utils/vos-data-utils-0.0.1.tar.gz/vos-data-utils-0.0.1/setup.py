import setuptools
from vdu import (
    author,
    version,
    description
)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vos-data-utils",
    version=version,
    author=author,
    author_email="dev@valueofspace.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vos-team/vos-data-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'shortcut1 = package.module:func',
        ],
        'gui_scripts': [
            'shortcut2 = package.module:func',
        ]
    }
)
