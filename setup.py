import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-x', 'tests']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.md', 'rb') as f:
    long_description = f.read().decode('utf-8')


requires = [
    'Flask==1.1.2',
    'Flask-Caching==1.8.0',
    'Flask-Cors==3.0.4',
    'Flask-JWT-Extended==3.9.1',
    'Flask-Migrate==2.2.1',
    'Flask-Redis==0.3.0',
    'Flask-RESTful==0.3.6',
    'Flask-SQLAlchemy==2.4.1',
    'loguru==0.2.5',
    'passlib==1.7.1',
    'PyMySQL==0.8.1',
    'redis>=3.2.0',
    'sqlalchemy>=1.3.0',
    'blinker==1.4',
    'celery==4.2.1',
    'click==6.7',
    'flasgger',
]

test_requirements = [
    'flower==0.9.2',
    'isort==4.3.4',
    'pre-commit==1.12.0',
    'pytest==3.8.0',
    'pytest-cov==2.5.1',
    'pytest-flake8==1.0.4',
    'tox==3.13.2',
    'coverage>=4.5.1',
]


setup(
    name='flask_cc_api',
    version='0.9.0.dev1',
    description="libs for flask-cc api projects",
    long_description=long_description,
    author='wen',
    author_email='w_angzhiwen@163.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    package_data={'': ['*.yaml']},
    include_package_data=True,
    zip_safe=False,

    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
        [console_scripts]
        flask_cc_api=flask_cc_api.cli.main:cli
    ''',

    install_requires=requires,
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
