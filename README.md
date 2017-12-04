# Pip Freezer
Author:Tim Santor <tsantor@xstudios.agency>

# Overview
For the organized developer. Puts packages in their proper place (base.txt, local.txt, production.txt, test.txt). **Playes nice with [Django Cookiecutter](https://github.com/pydanny/cookiecutter-django).**


# Installation
To install Pip Freezer, simply:

    pip install pipfreezer


## Usage
In the root of your prject, run:

```bash
pipfreezer
```

When installing requirments simply use:
```bash
pip install -r requirements/local.txt
```

> **NOTE:** On first run, `pipfreezer` will create a config file at `~/.pipfreezer/pipfreezer.cfg`. This contains the rules for where pipfreezer will place known requirements.  Feel free to edit this to your liking.

# Documentation
Documentation is available at TODO


# Version History
- **0.1.0** - Initial release


# Issues
If you experience any issues, please create an [issue](https://bitbucket.org/tsantor/pip-freezer/issues) on Bitbucket.
