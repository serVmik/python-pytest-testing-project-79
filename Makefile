lint:
	poetry run flake8 page_loader

build:
	poetry build

package-install:
	python3 -m install --user dist/*.whl
