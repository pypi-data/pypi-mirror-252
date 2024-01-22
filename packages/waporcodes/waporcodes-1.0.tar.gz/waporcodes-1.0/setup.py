#!/usr/bin/env python
"""Setup script for building nret's python bindings"""
import os
import codecs
import re
from os import path
from setuptools import setup, find_packages

# Global variables for this extension:
name = "waporcodes"  # name of the generated python extension (.so)
description = "A Python module to list FAO WaPOR data products and country codes."
long_description = "This module lists WaPOR products and country codes for level-3 products."# for one or multiple specified products within a given time period and a defined region based on a shapefile.."
author = "Solomon Seyoum, Mahmoud H. Ahmed,   @ IHE Delft, The Netherlands"
author_email = "s.seyoum@un-ihe.org, mahmoudhatim55@gmail.com"
url = "https://github.com/wateraccounting/WAPORWP/tree/v1.1"

setup(
    name=name,
    version= 1.0,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author,
    url=url,
    author_email=author_email,
    include_package_data=True,
    install_requires=[
        "requests",
        "pandas"

    ],
    packages=find_packages(),
    zip_safe=False 
)