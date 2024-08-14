# coding: utf-8

import io
import os

from setuptools import setup

REQUIRES = [
    "transformers>=4.42.0",
    "datasets",
    "accelerate>=0.33,<1.0.0",
    'typing>=3.6.4,<4.0.0; python_version<"3.5"',
]


dir = os.path.abspath(os.path.dirname(__file__))


about = {}
with io.open(os.path.join(dir, "__version__.py")) as f:
    exec(f.read(), about)


setup(
    name="yotta-labs",
    version=about["__version__"],
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=REQUIRES,
    python_requires=">=3.8",
    include_package_data=True,
)
