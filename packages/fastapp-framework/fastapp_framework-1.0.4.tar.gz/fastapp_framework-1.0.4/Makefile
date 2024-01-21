SRC_DIR = src/fastapp

.PHONY: run, run_dev
run_dev:
	docker-compose -f docker-compose-dev.yml up --build
run:
	docker-compose up --build

.PHONY: install_dev
install_dev:
	pip install -e .

.PHONY: lint, mypy, test, cov
lint:
	python -m pylint $(SRC_DIR)

mypy:
	python -m mypy $(SRC_DIR)

test:
	python -m pytest --cov-report html --cov-report term --cov=fastapp --cov-fail-under=80 src

cov:
	python -c "import webbrowser; webbrowser.open('http://localhost:8001')"
	python -m http.server --directory=./htmlcov 8001
