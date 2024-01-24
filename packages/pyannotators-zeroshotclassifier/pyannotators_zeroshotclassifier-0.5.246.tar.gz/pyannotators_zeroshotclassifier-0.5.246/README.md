# pyannotators_zeroshotclassifier

[![license](https://img.shields.io/github/license/oterrier/pyannotators_zeroshotclassifier)](https://github.com/oterrier/pyannotators_zeroshotclassifier/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_zeroshotclassifier/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_zeroshotclassifier/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_zeroshotclassifier)](https://codecov.io/gh/oterrier/pyannotators_zeroshotclassifier)
[![docs](https://img.shields.io/readthedocs/pyannotators_zeroshotclassifier)](https://pyannotators_zeroshotclassifier.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_zeroshotclassifier)](https://pypi.org/project/pyannotators_zeroshotclassifier/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_zeroshotclassifier)](https://pypi.org/project/pyannotators_zeroshotclassifier/)

Annotator based on Facebook's ZeroShotClassifier

## Installation

You can simply `pip install pyannotators_zeroshotclassifier`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_zeroshotclassifier
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
