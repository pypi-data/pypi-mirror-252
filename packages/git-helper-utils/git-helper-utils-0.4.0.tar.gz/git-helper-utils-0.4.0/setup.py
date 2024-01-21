#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "Rich"
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
    description="Collection of Python utility scripts to facilitate git related tasks.",
    entry_points={
        'console_scripts': [
            'create-git-branch=git_helper_utils.create_git_branch:main',
            'create-git-commit-file=git_helper_utils.create_git_commit_file:main',
            'make-git-helper-utils=git_helper_utils.make_shell_scripts_and_aliases:main',
        ]
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='git-helper-utils',
    name='git-helper-utils',
    packages=find_packages(include=['git_helper_utils', 'git_helper_utils.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/git-helper-utils',
    version='0.4.0',
    zip_safe=False,
)
