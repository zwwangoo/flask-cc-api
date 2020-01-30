from setuptools import find_packages, setup

with open('README.md', 'rb') as f:
    long_description = f.read().decode('utf-8')

with open('requirements-prod.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]


setup(
    name='flask_cc_api',
    version='0.9.0.dev1',
    description="libs for flask-cc api projects",
    long_description=long_description,
    author='wen',
    author_email='w_angzhiwen@163.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=requirements,
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
)
