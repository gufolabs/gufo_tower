# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# NOC Tower setup script
# -----------------------------------------------------------------------
# Copyright (C) 2015-1016 The NOC Project
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import os

from setuptools import setup, find_packages, findall
from setuptools.command.install import install

class TowerInstall(install):
    """
    Create additional directories
    """

    def run(self):
        install.run(self)
        # Create directories
        for d in ["db", "cache", "repo",
                  "log/jobs",
                  "log/crashinfo/collect",
                  "data/src_dist", "playbooks",
                  "ansible/cp", "crashinfo"]:
            path = os.path.join(self.prefix, "var", "tower", d)
            if not os.path.exists(path):
                os.makedirs(path)


def main():
    kwargs = {}

    with open("Readme.md") as f:
        kwargs["long_description"] = f.read()

    with open("VERSION") as f:
        VERSION = f.read().strip()

    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
        requirements = [x.strip() for x in requirements if x.strip()]

    tower_data = findall(os.path.join("tower", "ui"))
    tower_data = [
        x[6:] for x in tower_data
        if not x.endswith("_debug.js") and not x.endswith(".js.map")
    ]

    setup(
        name="noc-tower",
        version=VERSION,
        description="NOC Tower",
        author="Dmitry Volodin",
        maintainer="Aleksey Shirokih",
        license="BSD",
        author_email="info@nocproject.org",
        url="https://bitbucket.org/nocproject/noc-tower",
        cmdclass={
            "install": TowerInstall
        },
        packages=find_packages(exclude=["tests"]),
        entry_points={
            "console_scripts": [
                "tower-inv = tower.cli.inv:main",
                "tower-pull = tower.cli.pull:main",
                "tower-web = tower.daemons.web:run",
                "tower-dump = tower.cli.backup:dump",
                "tower-restore = tower.cli.backup:restore",
                "tower-joblog = tower.cli.joblog:main",
                "tower-deploy = tower.cli.deploy:main",
            ]
        },
        package_data={
            "tower": tower_data
        },
        data_files=["VERSION"],
        install_requires=requirements,
        setup_requires=['wheel'],
        zip_safe=False,
        classifiers=[
            "Operating System :: Unix",
            "Environment :: Console",
            "Environment :: Web Environment"
            "Programming Language :: Python :: 3.8"
        ],
        **kwargs
    )


if __name__ == "__main__":
    main()
