from setuptools import find_packages
from setuptools import setup

NAME = "braze-client-p311"
VERSION = "0.0.4"

REQUIRES = ["requests >=2.21.0, <3.0.0", "tenacity ==8.2.3"]

EXTRAS = {"dev": ["tox"]}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="Braze Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpeutcr8/braze-client",
    author_email="kpeutcr8@yandex.ru",
    keywords=["Appboy", "Braze"],
    install_requires=REQUIRES,
    extras_require=EXTRAS,
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
)
