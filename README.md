# Pip Freezer

![Coverage](https://img.shields.io/badge/coverage-70%25-brightgreen)

<!-- ![Code Style](https://img.shields.io/badge/code_style-ruff-black) -->

## Overview

For the organized, but lazy developer, meaning that you'll update a package, but you don't want to be bothered with updating the requirements file. Pip Freezer pins packages no matter which requirements file they live in and maintains your comments and line breaks.

> NOTE: Plays nice with [Django Cookiecutter](https://github.com/pydanny/cookiecutter-django).

## Background

We all have our preferences with how we manage package dependencies. There is the awesome [Poetry](https://python-poetry.org/), but there are still those of us who like to manually manage requirements with comments in various files such as `requirements.txt`, `requirements_dev.txt`. `requirements_test.txt`, or even `requirements/base.txt`, `requirements/local.txt` and `requirements/production.txt` or other similar variations.

Simply running `pip freeze > requirements.txt` is not of much use if you like to be organized and only pin what you've manually defined as a "top-level" dependency (and not its sub-dependencies).

Running `pipfreezer` will only pin packages defined in your requirements files.

> NOTE: `pipfreezer` does not do any upating of packages itself, you can use `pip install -U package-name` or something like [pip-review](https://pypi.org/project/pip-review/). You would manually update packages and then run `pipfreezer` to auto-update those in your requirements files.

## Installation

To install Pip Freezer, simply use pip:

```bash
$ python3 -m pip install pip-freezer
```

## Usage

In the root of your project, run:

```bash
# Freeze only packages defined in your requirements files.
pipfreezer

# Update only the packages defined in your requirements files.
pipfreezer-upgrade
```

> NOTE: `pipfreezer` will **not** add or pin packages that you **have not already defined** in one of your requirements files. **This is intentional**.

## Development

```bash
make env
make pip_install
make pip_install_editable
```

## Testing

```bash
make pytest
make coverage
make open_coverage
```

## Issues

If you experience any issues, please create an [issue](https://github.com/tsantor/pip-freezer/issues) on Github.
