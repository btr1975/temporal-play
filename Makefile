# Makefile for project needs
# Author: Ben Trachtenberg
# Version: 2.0.1
#

.PHONY: all info build build-container coverage format pylint pytest start-container stop-container remove-container \
        gh-pages check-vuln pip-export mypy

info:
	@echo "make options"
	@echo "    all                 To run coverage, format, pylint, and check-vuln"
	@echo "    build               To build a distribution"
	@echo "    build-container     To build a container image"
	@echo "    check-vuln          To check for vulnerabilities in the dependencies"
	@echo "    check-security      To check for vulnerabilities in the code"
	@echo "    coverage            To run coverage and display ASCII and output to htmlcov"
	@echo "    format              To format the code with black"
	@echo "    mypy                To run mypy"
	@echo "    pylint              To run pylint"
	@echo "    pytest              To run pytest with verbose option"
	@echo "    start-container     To start the container"
	@echo "    stop-container      To stop the container"
	@echo "    remove-container    To remove the container"
	@echo "    gh-pages           To create the GitHub pages"



all: format pylint mypy coverage check-security pip-export

build:
	@uv build --wheel --sdist

coverage:
	@uv run pytest --cov --cov-report=html -vvv

format:
	@uv run black temporal_play/
	@uv run black tests/

pylint:
	@uv run pylint temporal_play/

pytest:
	@uv run pytest --cov -vvv

check-security:
	@uv run bandit -c pyproject.toml -r .

mypy:
	@uv run mypy temporal_play/

pip-export:
	@uv export --no-dev --no-emit-project --no-editable > requirements.txt
	@uv export --no-emit-project --no-editable > requirements-dev.txt


gh-pages:
	@rm -rf ./docs/source/code
	@uv run sphinx-apidoc -o ./docs/source/code ./temporal_play
	@uv run sphinx-build ./docs ./docs/gh-pages





build-container:
	@cd containers && podman build --ssh=default --build-arg=build_branch=main -t temporal-play:latest -f Containerfile

start-container:
	@podman run -itd --name temporal-play -p 8080:8080 localhost/temporal-play:latest

stop-container:
	@podman stop temporal-play

remove-container:
	@podman rm temporal-play



