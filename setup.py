#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='shared',
      version='0.0.1',
      description='The package shares fast download api',
      author='Itamar Farchy',
      author_email='itamar.farchy@email.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      license='LICENSE',
    )
