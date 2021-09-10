python_version=3.9.4
venv=pipfreezer_env

env:
	pyenv virtualenv ${python_version} ${venv} && pyenv local ${venv}

reqs:
	python -m pip install -U pip && python -m pip install -r requirements.txt \
	&& python -m pip install -r requirements_dev.txt

clean:
	rm -rf {build,dist,*.egg-info,htmlcov}
	rm -rf {mkdocs/site,docs/site}
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;

destroy_env:
	pyenv uninstall ${venv}

build:
	python setup.py sdist bdist_wheel

upload_test:
	python setup.py sdist bdist_wheel && twine upload dist/* -r pypitest

upload:
	python setup.py sdist bdist_wheel && twine upload dist/* -r pypi
