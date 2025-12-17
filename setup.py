
# this is the pyproject.toml file for the cfs package
# WHAT IS THIS FILE?
# This file is used to define the build system requirements and project metadata for the cfs package

# WHY IS THIS FILE NEEDED?
# It specifies the tools and dependencies needed to build and install the package, ensuring consistency across different
# environments.
# when the command `pip install -e.` is run, pip reads this file to determine how to build and install the package.

from setuptools import setup, find_packages

setup(
    name="cfs-cli",
    version="0.1.0",
    packages=find_packages(include=["cfs", "cfs.*"]),
    include_package_data=True,
    package_data={
        "" : ["modules/templates/*/*"],
    },
    install_requires=[
        "click",
        "jinja2",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "cfs=cfs_cli.cli:main",
        ],
    },
)
