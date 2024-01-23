# isopsephism

[![PyPI](https://img.shields.io/pypi/v/isopsephism.svg)](https://pypi.org/project/isopsephism/)
[![Tests](https://github.com/uggerus/isopsephism/actions/workflows/test.yml/badge.svg)](https://github.com/uggerus/isopsephism/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/uggerus/isopsephism?include_prereleases&label=changelog)](https://github.com/uggerus/isopsephism/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/uggerus/isopsephism/blob/main/LICENSE)

Find the numerical value of words.

## Installation

Install this library using `pip`:
```bash
pip install isopsephism
```
## Usage

```
from isopsephism.isopsephism import isopsephy
print(isopsephy.convert_word_to_num("ΚΟΥΡΑΙ"))
#prints 601
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd isopsephism
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
