from setuptools import find_packages, setup

setup(
    name='cc_api',
    version='0.0.3',
    description="libs for cc api projects",
    author='wen',
    author_email='w_angzhiwen@163.com',
    packages=find_packages(exclude=[]),
    install_requires=[],
    zip_safe=True,
    entry_points='''
        [console_scripts]
        cc_api=cc_api.cli.main:cli
    '''
)
