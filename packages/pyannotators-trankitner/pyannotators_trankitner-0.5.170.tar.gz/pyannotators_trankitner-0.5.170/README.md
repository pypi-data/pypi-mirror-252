# pyannotators_trankitner

[![license](https://img.shields.io/github/license/oterrier/pyannotators_trankitner)](https://github.com/oterrier/pyannotators_trankitner/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_trankitner/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_trankitner/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_trankitner)](https://codecov.io/gh/oterrier/pyannotators_trankitner)
[![docs](https://img.shields.io/readthedocs/pyannotators_trankitner)](https://pyannotators_trankitner.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_trankitner)](https://pypi.org/project/pyannotators_trankitner/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_trankitner)](https://pypi.org/project/pyannotators_trankitner/)

Annotator based on Facebook's TrankitNER

## Installation

You can simply `pip install pyannotators_trankitner`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_trankitner
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
