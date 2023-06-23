# Pip Freezer
Author:Tim Santor <tsantor@xstudios.com>

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
pip install pip-freezer
```

## Usage
In the root of your project, run:

```bash
pipfreezer
```

> NOTE: `pipfreezer` will **not** add or pin packages that you **have not already defined** in one of your requirements files. **This is intentional**.

# Issues
If you experience any issues, please create an [issue](https://bitbucket.org/tsantor/pip-freezer/issues) on Bitbucket.
