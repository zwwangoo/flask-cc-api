.PHONY: run install check migrate-init migrate-db test clean new-user celery

pyenv_position = $(shell whereis pyenv)

ifneq ($(pyenv_position), pyenv:)
	python_position = $(shell pyenv which python)
	python_version = $(shell python -V | awk -F ' ' '{print substr($$2,0,3)}')
	python_path = $(python_position)$(python_version)
endif

check:
	@echo 'Checking...'
ifneq ($(pyenv_position), pyenv:)
	@[ -f $(python_path) ] || (ln -s $(python_position) $(python_path) && echo 'Made symbolic link $(python_path)')
	@[ -d flask_cc_api/instance ] || (echo 'Error: You must create an folder named instance at root of project.Then create flask_cc_api/instance/__init__.py and flask_cc_api/instance/secret.py.')
	@[ -f flask_cc_api/instance/dev.py ] || (echo 'Error: You must create an file named cc_ap/instance/dev.py.')
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
	@flask_cc_api db init -d dev/migrations
	@echo 'Done [migrate-init]'
endif

migrate-db: migrate-init
	@echo 'Migrating database.'
	@flask_cc_api db upgrade -d dev/migrations
	@flask_cc_api db migrate -d dev/migrations
	@flask_cc_api db upgrade -d dev/migrations
	@echo 'Done [migrate-db]'

run:
	@flask_cc_api run --debugger --reload --with-threads -h 0.0.0.0

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
	@find . -name 'beat.*' -print -exec rm -rf {} + 
	@find . -path ./.coveragerc -prune -o -name '*coverage*' -print -exec rm -f {} +
	@echo 'Done [clean]'

test: clean
	@tox

new-user:
	@flask_cc_api new_user

celery:
	@celery -B -A celery_worker.celery worker --loglevel=info -s ./flask_cc_api/proj/schedule/beat

