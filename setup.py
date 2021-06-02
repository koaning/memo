import os
from setuptools import setup, find_packages

base_packages = ["rich>=9.2.0", "orjson>=3.4.5", "joblib>=1.0.1"]

test_packages = [
    "flake8>=3.6.0",
    "pytest>=4.0.2",
    "numpy>=1.19.4",
    "mktestdocs>=0.1.0",
    "tqdm>=4.54.0",
] + base_packages

util_packages = [
    "jupyter>=1.0.0",
    "jupyterlab>=0.35.4",
]

docs_packages = [
    "mkdocs==1.1.2",
    "mkdocs-material==6.1.6",
    "mkdocstrings==0.13.6",
]

dev_packages = util_packages + docs_packages + test_packages

web_packages = ["httpx>=0.16.1"] + base_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="memo",
    version="0.2.1",
    packages=find_packages(exclude=["notebooks"]),
    install_requires=base_packages,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    extras_require={
        "web": web_packages,
        "test": test_packages,
        "dev": dev_packages,
    },
)
