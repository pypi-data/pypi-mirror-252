from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.2"
DESCRIPTION = "Unofficial python package for ActionNetwork (https://actionnetwork.org/)"
LONG_DESCRIPTION= "Basic package"

setup(name="actionnetworkpy",
      author="Nir Tatcher",
      author_email="<nirto111@gmail.com>",
      description=DESCRIPTION,
      packages=find_packages(),
      keywords=["python","action_network", "ActionNetwork", "actionnetwork", "AN", "an"]
      )
