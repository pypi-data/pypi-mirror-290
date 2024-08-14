.PHONY: test

test:
	python -m unittest discover -s tests -p 'test_*.py'

build:
	python -m build


upload-test:
	python -m twine upload -r testpypi dist/*

publish:
	python -m twine upload dist/*
