from setuptools import setup, find_packages
import codecs
import os

VERSION = "1.1.9"
DESCRIPTION = "Unofficial python package for ActionNetwork (https://actionnetwork.org/)"

setup(name="py-actionnetworkorg",
      version=VERSION,
      author="Nir Tatcher",
      author_email="<nirto111@gmail.com>",
      description=DESCRIPTION,
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      keywords=["python","action_network", "ActionNetwork", "actionnetwork", "AN", "an"],
      classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      install_requires=[
            "psycopg2_binary==2.9.6",
            "Requests==2.31.0",
            "setuptools==65.5.0",
            "sshtunnel==0.4.0",
      ],
      url="https://github.com/NirTatcher/actionnetworkpy.git",
      )
