# vereqsyn

[![Test](https://github.com/minddistrict/vereqsyn/actions/workflows/tests.yml/badge.svg)](https://github.com/minddistrict/vereqsyn/actions/workflows/tests.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/vereqsyn.svg)](https://pypi.org/project/vereqsyn)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vereqsyn.svg)](https://pypi.org/project/vereqsyn)

Bi-directional versions.cfg <–> requirements.txt synchronization

This program can be used to synchronize a `versions.cfg` used by
[zc.buildout](https://pypi.org/project/zc.buildout/) with a `requirements.txt`
as used by [pip](https://pypi.org/project/pip/).

This is be helpful to keep using `zc.buildout` but get version updates via
GitHub's Dependabot.

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Constraints](#constraints)
- [Hacking](#hacking)
- [License](#license)

## Installation

```console
pip install vereqsyn
```

## Usage

```console
vereqsyn --help
vereqsyn versions.cfg requirements.txt
```

## Constraints

* `versions.cfg` is the source of truth. `requirements.txt` can get recreated.
* So `versions.cfg` can contain comments, the ones in `requirements.txt` are
  lost when running recreate.

## Hacking

### Run the tests

```console
hatch run cov
```

## License

`vereqsyn` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
