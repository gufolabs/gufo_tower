# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# NOC Tower setup script
# -----------------------------------------------------------------------
# Copyright (C) 2015 The NOC Project
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
from setuptools import setup


def main():
    kwargs = {}

    with open("README.md") as f:
        kwargs["long_description"] = f.read()

    with open("VERSION") as f:
        VERSION = f.read().strip()

    setup(
        name="noc-tower",
        version=VERSION,
        description="NOC Tower",
        author="Dmitry Volodin",
        # license="BSD",
        author_email="info@nocproject.org",
        url="https://bitbucket.org/nocproject/noc-tower",
        packages=[
            "tower",
            "tower.inv"
        ],
        entry_points={
            "console_scripts": [
                "inv = tower.inv.commands:inv",
                "tower-web = tower.daemons.web:run"
            ]
        },
        zip_safe=False,
        classifiers=[
            "Operating System :: Unix",
            "Environment :: Console",
            "Environment :: Web Environment"
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7"
        ],
        **kwargs
    )


if __name__ == "__main__":
    main()
