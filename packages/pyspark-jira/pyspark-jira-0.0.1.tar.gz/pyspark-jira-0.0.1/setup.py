#!/usr/bin/env python
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


dist = setup(
    name='pyspark-jira',
    version="0.0.1",
    description='PySpark JIRA Data Source',
    author='Hyukjin Kwon',
    author_email='gurwls223@apache.org',
    url='https://github.com/HyukjinKwon/pyspark-jira',
    license='Apache License 2.0',
    packages=['pyspark_jira'],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    test_suite='tests',
    python_requires='>=3.10',
)
