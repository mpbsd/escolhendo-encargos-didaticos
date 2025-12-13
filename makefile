help:
	python3 -m pkgs.core --help

%:
	python3 -m pkgs.core --lump $@

black:
	isort pkgs/core.py
	black -l 79 pkgs/core.py
	isort pkgs/xpdf.py
	black -l 79 pkgs/xpdf.py

clean:
	find . -type d -name __pycache__ | xargs rm -rf

ready:
	python3 -m venv venv; \
	. venv/bin/activate; \
	pip install -U pip; \
	pip install -r requirements.txt; \
	deactivate

.PHONY: help black clean ready
