#!/usr/bin/env python3

from setuptools import setup
from doctorapp import __version__


deps = ["boto3==1.6.6",
        "CherryPy==14.0.0"]


setup(name='doctorapp',
      version=__version__,
      description='doctorapp - Devops Challenge',
      url='https://github.com/dpedu/devops-challenge',
      author='dpedu',
      author_email='dave@davepedu.com',
      packages=['doctorapp'],
      install_requires=deps,
      entry_points={
          "console_scripts": [
              "doctorappd = doctorapp.app:main"
          ]
      })
