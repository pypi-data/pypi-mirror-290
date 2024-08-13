from setuptools import setup
import os

VERSION = "2.0.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="ai4-metadata-validator",
    description="ai4-metadata-validator is now ai4-metadata",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["ai4-metadata"],
    classifiers=["Development Status :: 7 - Inactive"],
)
