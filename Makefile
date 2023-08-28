install:
	poetry install

lint:
	poetry run flake8

test:
	poetry run pytest --cov=page_loader -vv -s

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

check: lint test

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl
