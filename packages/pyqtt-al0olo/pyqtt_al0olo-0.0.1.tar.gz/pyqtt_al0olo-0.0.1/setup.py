#!/usr/bin/python3
import sys
from os import path

from setuptools import find_packages, setup

import pyqtt

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()

extra = {}
if sys.version_info >= (3, 4):
    extra["use_2to3"] = False
    extra["convert_2to3_doctests"] = ["README.md"]

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

KEYWORDS = "Pyqtt MQTT client."

TESTS_REQUIRE = [
    "atomicwrites>=1.3.0",
    "attrs>=19.1.0",
    "codecov>=2.0.15",
    "coverage>=4.5.3",
    "more-itertools>=7.0.0",
    "pluggy>=0.11.0",
    "py>=1.8.0",
    "pytest-asyncio>=0.12.0",
    "pytest-cov>=2.7.1",
    "pytest>=5.4.0",
    "six>=1.12.0",
    "uvloop>=0.14.0",
]

# Allow you to run pip install .[test] to get test dependencies included
EXTRAS_REQUIRE = {"test": TESTS_REQUIRE}

setup(
    name="pyqtt_al0olo",
    version=pyqtt.__version__,
    description="Client for MQTT protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=pyqtt.__author__,
    author_email=pyqtt.__email__,
    license='MIT',
    url="https://github.com/al0olo/pyqtt",
    packages=find_packages(exclude=['examples', 'tests']),
    download_url="https://github.com/al0olo/pyqtt",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    zip_safe=True,
    test_suite="tests",
    install_requires=[],
    tests_require=TESTS_REQUIRE,
    extras_require=EXTRAS_REQUIRE,
    python_requires='>=3.5',
)
