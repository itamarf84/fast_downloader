#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='fast_downloader',
      version='0.0.1',
      description='The package shares fast download api',
      author='Itamar Farchy',
      author_email='itamar.farchy@email.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      license='LICENSE',
      url="https://github.com/itamarf84/fast_downloader",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          "Programming Language :: Python :: 3",
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Internet :: WWW/HTTP',
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      )
