clean:
	rm -fr htmlcov
	rm -fr dist
	rm -fr build
	rm -fr .eggs
	rm -fr *.egg-info
	rm -fr mkdocs/site
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;

test:
	python setup.py sdist bdist_wheel && twine upload dist/* -r pypitest

publish:
	python setup.py sdist bdist_wheel && twine upload dist/* -r pypi

clean:
