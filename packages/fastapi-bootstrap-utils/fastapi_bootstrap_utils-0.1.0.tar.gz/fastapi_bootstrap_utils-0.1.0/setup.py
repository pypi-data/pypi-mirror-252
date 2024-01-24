#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "PyYAML",
    "Rich",
]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tools for bootstrapping simple REST API using FastAPI for serving data files",
    entry_points={
        'console_scripts': [
            'create-app=fastapi_bootstrap_utils.create_app:main',
            'make-fastapi-bootstrap-utils=fastapi_bootstrap_utils.make_shell_scripts_and_aliases:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fastapi-bootstrap-utils',
    name='fastapi_bootstrap_utils',
    packages=find_packages(include=['fastapi_bootstrap_utils', 'fastapi_bootstrap_utils.*']),
    package_data={
        "fastapi_bootstrap_utils": [
            "conf/config.yaml",
            "templates/main.py.tt",
            "templates/helper.py.tt",
            "templates/router.py.tt",
        ]
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/fastapi-bootstrap-utils',
    version='0.1.0',
    zip_safe=False,
)
