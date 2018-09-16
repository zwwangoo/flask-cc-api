.PHONY: run install check

pyenv_position = $(shell whereis pyenv)

ifneq ($(pyenv_position), pyenv:)
	python_position = $(shell pyenv which python)
	python_version = $(shell python -V | awk -F ' ' '{print substr($$2,0,3)}')
	python_path = $(python_position)$(python_version)
endif

check:
	@echo 'Checking...'
ifneq ($(pyenv_position), pyenv:)
	@[ -f $(python_path) ] || (ln -sr $(python_position) $(python_path) && echo 'Made symbolic link $(python_path)')
	@[ -d instance ] || (echo 'Error: You must create an folder named instance at root of project.Then create instance/__init__.py and instance/secret.py.')
	@[ -f instance/dev.py ] || (echo 'Error: You must create an file named instance/dev.py.')
	@[ -f .python-version ] || (echo 'Suggestion: You must give an file named .python-version if you use pyenv and virtualenv.')
	@echo 'Done [check]'
else
	@echo "Error: You should use pyenv. [https://github.com/pyenv/pyenv]"
endif

run:
	@python wsgi.py

install:requirements.txt
	@echo 'Installing requirements.'
	@pip install -U pip
	@pip install -r requirements.txt
	@echo 'Done'
