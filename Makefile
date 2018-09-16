.PHONY: run install

run:
	@python wsgi.py

install:requirements.txt
	@echo 'Installing requirements.'
	@pip install -U pip
	@pip install -r requirements.txt
	@echo 'Done'
