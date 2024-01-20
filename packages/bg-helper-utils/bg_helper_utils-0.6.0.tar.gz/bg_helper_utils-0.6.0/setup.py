#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "Rich",
    "PyYAML",
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
    description="Collection of Python convenience scripts for BG tasks.",
    entry_points={
        'console_scripts': [
            'find-samplesheet=bg_helper_utils.find_samplesheet:main',
            'find-batch-analysis-dir=bg_helper_utils.find_batch_analysis_dir:main',
            'make-bg-helper-utils=bg_helper_utils.make_shell_scripts_and_aliases:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bg_helper_utils',
    name='bg_helper_utils',
    packages=find_packages(include=['bg_helper_utils', 'bg_helper_utils.*']),
    package_data={"bg_helper_utils": ["conf/config.yaml"]},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/bg-helper-utils',
    version='0.6.0',
    zip_safe=False,
)
