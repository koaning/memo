from setuptools import setup, find_packages

base_packages = ["rich>=9.2.0", "orjson>=3.4.5"]

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
    "mkdocs>=1.1",
    "mkdocs-material>=4.6.3",
    "mkdocstrings>=0.8.0",
]

dev_packages = util_packages + docs_packages + test_packages

web_packages = ["httpx>=0.16.1"] + base_packages

setup(
    name="memo",
    version="0.1.3",
    packages=find_packages(exclude=["notebooks"]),
    install_requires=base_packages,
    extras_require={
        "web": web_packages,
        "test": test_packages,
        "dev": dev_packages,
    },
)
