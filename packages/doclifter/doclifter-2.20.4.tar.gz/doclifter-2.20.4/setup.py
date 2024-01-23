#!/usr/bin/env python

import sys

from setuptools import setup

sys.path.insert(0, "src")
from doclifter import version

name = "doclifter"


setup(
    name=name,
    version="2.20.4",
    author="Eric S. Raymond",
    author_email="esr@thyrsus.com",
    maintainer="Mingzhe Zou",
    maintainer_email="zoumingzhe@outlook.com",
    description="Lift documents in {n,t}roff markups to XML-DocBook.",
    long_description_content_type="text/plain",
    long_description=open("README").read(),
    url="https://gitlab.com/esr/doclifter",
    data_files=[("share/man/man1", ["doclifter.1.gz"])],
    package_dir={"": "src"},
    scripts=[name],
)
