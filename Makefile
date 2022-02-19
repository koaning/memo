black:
	black memo tests setup.py

flake:
	flake8 memo tests setup.py

test:
	pytest

check: black flake test

install:
	python -m pip install -e ".[dev]"
	pre-commit install

install-test:
	python -m pip install -e ".[test]"
	python -m pip install -e ".[all]"

pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

clean:
	rm *.jsonl *.json