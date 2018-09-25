.PHONY: run install check migrate-init migrate-db test clean

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
	@[ -d cc_api/instance ] || (echo 'Error: You must create an folder named instance at root of project.Then create cc_api/instance/__init__.py and cc_api/instance/secret.py.')
	@[ -f cc_api/instance/dev.py ] || (echo 'Error: You must create an file named cc_ap/instance/dev.py.')
	@[ -f .python-version ] || (echo 'Suggestion: You must give an file named .python-version if you use pyenv and virtualenv.')
	@echo 'Done [check]'
else
	@echo "Error: You should use pyenv. [https://github.com/pyenv/pyenv]"
endif

install:requirements.txt
	@echo 'Installing requirements.'
	@pip install -U pip
	@pip install -r requirements.txt
	@echo 'Done'

migrate-init: install
ifeq (dev/migrations, $(wildcard dev/migrations))
	@echo 'SKIP [migrate-init]'
	@echo 'REASON: Database has already been initialised.'
else
	@echo 'Init database migration.'
	@cc_api db init -d dev/migrations
	@echo 'Done [migrate-init]'
endif

migrate-db: migrate-init
	@echo 'Migrating database.'
	@cc_api db upgrade -d dev/migrations
	@cc_api db migrate -d dev/migrations
	@cc_api db upgrade -d dev/migrations
	@echo 'Done [migrate-db]'

run:
	@cc_api run --debugger --reload --with-threads -h 0.0.0.0

clean:
	@echo 'removing...'
	@find . -name '.tox' -print -exec rm -rf {} +
	@find . -name 'dist' -print -exec rm -rf {} +
	@find . -name 'htmlcov' -print -exec rm -rf {} +
	@find . -name '*.pyc' -print -exec rm -f {} +
	@find . -name '*.pyo' -print -exec rm -f {} +
	@find . -name '*.log' -print -exec rm -f {} +
	@find . -name '.pytest_cache' -print -exec rm -rf {} +
	@find . -name '__pycache__' -print -exec rm -rf {} +
	@find . -path ./.coveragerc -prune -o -name '*coverage*' -print -exec rm -f {} +
	@echo 'Done [clean]'

test: clean
	@tox

