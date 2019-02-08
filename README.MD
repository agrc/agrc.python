# AGRC Python Package

A collection of python modules that make life easier for us at AGRC (except @steveoh who's on a whole different level than the rest of us).

## Installation

`pip install agrc`

## Development

Restore `UPDATE_TESTS.bak` as a local SDE database if needed.

To run tests: `tox`

## To Publish a new version to Pypi

1. increment the version number in setup.py file
1. update CHANGES.txt file
1. Commit your changes
1. run python `setup.py sdist upload`
