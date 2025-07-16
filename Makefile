VENV ?= .venv
PYTHON := python3
PIP := $(VENV)/bin/pip

$(VENV)/bin/python:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

install: $(VENV)/bin/python

run: install
	$(VENV)/bin/python main_gui.py

clean:
	rm -rf $(VENV)

.PHONY: install run clean