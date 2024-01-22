import io
import os
from setuptools import find_packages, setup

def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content

def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]

setup(
    name="studip-cli",
    version="0.0.1",  # Directly specify the version here
    description="StudIP command line interface to emulate a JSON API",
    url="https://github.com/FrederikRichter/StudIP-cli",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Frederik Richter",
    packages=find_packages(exclude=["tests", ".github"]),
    entry_points={
        "console_scripts": ["studip-cli = app.__main__:main"]
    },
    # Include the setup hook
    setup_requires=["setuptools>=46.1.0", "wheel>=0.36.2"],
    python_requires=">=3.6",
)
