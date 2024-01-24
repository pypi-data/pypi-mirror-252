# pep610

[![PyPI - Version](https://img.shields.io/pypi/v/pep610.svg)](https://pypi.org/project/pep610)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pep610.svg)](https://pypi.org/project/pep610)
[![codecov](https://codecov.io/gh/edgarrmondragon/pep610/graph/badge.svg?token=6W1M6P9LYI)](https://codecov.io/gh/edgarrmondragon/pep610)
[![Documentation Status](https://readthedocs.org/projects/pep610/badge/?version=latest)](https://pep610.readthedocs.io/en/latest/?badge=latest)

[PEP 610][pep610] specifies how the Direct URL Origin of installed distributions should be recorded.

The up-to-date, [canonical specification][pep610-pypa] is maintained on the [PyPA specs page][pypa-specs].

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install pep610
```

## Usage

You can use `pep610.read_from_distribution` to parse the [Direct URL Origin structure][pep610-structure] from a `Distribution` object:

```python
from importlib import metadata

import pep610

dist = metadata.distribution("pep610")
data = pep610.read_from_distribution(dist)

if isinstance(data, pep610.DirData) and data.dir_info.is_editable():
    print("Editable install")
else:
    print("Not editable install")
```

Or, in Python 3.10+ using pattern matching:

```python
from importlib import metadata

import pep610

dist = metadata.distribution("pep610")
data = pep610.read_from_distribution(dist)

match data:
    case pep610.DirData(url, pep610.DirInfo(editable=True)):
        print("Editable install")
    case _:
        print("Not editable install")
```

## License

`pep610` is distributed under the terms of the [Apache License 2.0](LICENSE).

[pep610]: https://www.python.org/dev/peps/pep-0610/
[pep610-pypa]: https://packaging.python.org/en/latest/specifications/direct-url/#direct-url
[pep610-structure]: https://packaging.python.org/en/latest/specifications/direct-url-data-structure/
[pypa-specs]: https://packaging.python.org/en/latest/specifications/
