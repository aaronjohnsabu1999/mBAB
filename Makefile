SHELL := /bin/bash

run:
	source venv/bin/activate && python app.py

install: venv
	source venv/bin/activate && make requirements

venv: 
	sudo apt install virtualenv
	virtualenv venv

requirements:
	pip install -r requirements.txt