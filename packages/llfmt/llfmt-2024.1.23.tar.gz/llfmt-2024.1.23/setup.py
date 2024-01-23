from setuptools import setup, find_packages
import os

VERSION = "2024.1.23"


def get_long_description():
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
            encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="llfmt",
    description=(
        "Simple tool for formatting code for LLMs."
    ),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Max Conradt",
    url="https://github.com/mhconradt/llfmt",
    project_urls={
        "Documentation": "https://github.com/mhconradt/llfmt/blob/main/README.md",
        "Issues": "https://github.com/mhconradt/llfmt/issues",
        # "CI": "https://github.com/mhconradt/llfmt/actions",
        "Changelog": "https://github.com/mhconradt/llfmt/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        llfmt=llfmt.__main__:main
    """,
    install_requires=[],
    extras_require={
        "test": [
            "pytest",
            "twine",
        ],
    },
    python_requires=">=3.7",
)
