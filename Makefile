clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -d -name '__pycache__' -exec rmdir {} +

clean: clean-pyc
	rm -rf .pytest_cache
	rm -rf *.egg-info

install:
	pip install -e .

test:
	pytest tests
