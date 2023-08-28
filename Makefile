install:
	poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --cov=page_loader -vv -s

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

check: lint test

build:
	poetry build

package-install:
	python3 -m install --user dist/*.whl
