from memo import __version__
from setuptools import setup, find_packages

base_packages = []

test_packages = [
    "flake8>=3.6.0",
    "pytest>=4.0.2",
]

util_packages = [
    "jupyter>=1.0.0",
    "jupyterlab>=0.35.4",
]

docs_packages = [
    "mkdocs>=1.1",
    "mkdocs-material>=4.6.3",
    "mkdocstrings>=0.8.0",
]

dev_packages = util_packages + docs_packages + test_packages

wandb_packages = ["wandb>=0.10.11"]

web_packages = ["httpx>=0.16.1"]

setup(
    name="memo",
    version=__version__,
    packages=find_packages(exclude=["notebooks"]),
    install_requires=base_packages,
    extras_require={
        "web": web_packages,
        "wandb": wandb_packages,
        "test": test_packages,
        "dev": dev_packages
    },
)
