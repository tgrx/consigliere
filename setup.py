#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

# Package meta-data.
NAME = "consigliere"
DESCRIPTION = "A library to build Telegram bots"
URL = "https://github.com/tgrx/consigliere"
EMAIL = "alexander@sidorov.dev"
AUTHOR = "Alexander Sidorov"
PYTHON_REQUIRES = ">=3.9.0"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "pydantic",
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License,
# remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    version_file = os.path.join(here, project_slug, "__version__.py")
    with open(version_file) as f:
        exec(f.read(), about)  # noqa: S102,DUO105
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(msg):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(msg))  # noqa: T001

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(  # noqa: S605,DUO106
            "{0} setup.py sdist bdist_wheel --universal".format(sys.executable)
        )

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")  # noqa: S605,S607,DUO106

        self.status("Pushing git tags…")
        version = about["__version__"]
        os.system(f"git tag v{version}")  # noqa: S605,DUO106
        os.system("git push --tags")  # noqa: S605,S607,DUO106

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=PYTHON_REQUIRES,
    url=URL,
    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*",
            "pyproject.toml",
            "tests",
            "tests.*",
        ]
    ),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
