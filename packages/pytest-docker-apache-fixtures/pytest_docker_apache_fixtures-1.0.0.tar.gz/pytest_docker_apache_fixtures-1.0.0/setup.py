#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


def find_version(*segments):
    root = os.path.abspath(os.path.dirname(__file__))
    abspath = os.path.join(root, *segments)
    with open(abspath, "r") as file:
        content = file.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", content, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string!")


setup(
    author="Richard Davis",
    author_email="crashvb@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    description="Pytest fixtures for testing with apache2 (httpd).",
    entry_points={
        "pytest11": ["docker_apache_fixtures = pytest_docker_apache_fixtures"]
    },
    extras_require={
        "dev": [
            "black",
            "coveralls",
            "pylint",
            "pytest",
            "pytest-cov",
            "twine",
            "wheel",
        ]
    },
    include_package_data=True,
    install_requires=[
        "bcrypt",
        "certifi",
        "docker",
        "lovely-pytest-docker",
        "pyopenssl",
        "pytest",
    ],
    keywords="apache apache2 docker fixtures httpd pytest",
    license="Apache License 2.0",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    name="pytest_docker_apache_fixtures",
    packages=find_packages(),
    package_data={
        "pytest_docker_apache_fixtures": ["docker-compose*.yml", "apache.*.cfg"]
    },
    project_urls={
        "Bug Reports": "https://github.com/crashvb/pytest-docker-apache-fixtures/issues",
        "Source": "https://github.com/crashvb/pytest-docker-apache-fixtures",
    },
    tests_require=["pytest"],
    test_suite="tests",
    url="https://github.com/crashvb/pytest-docker-apache-fixtures",
    version=find_version("pytest_docker_apache_fixtures", "__init__.py"),
)
