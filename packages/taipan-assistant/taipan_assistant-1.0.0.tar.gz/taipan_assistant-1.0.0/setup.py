from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="taipan-assistant",
    version="1.0.0",
    description="Package provides a simple CLI tool to be used as a personal assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7, <4",
    entry_points={  # Optional
        "console_scripts": [
            "taipan-assistant=main:main",
        ],
    },
    packages=find_packages(include=['search', 'record', 'notebook']),
)