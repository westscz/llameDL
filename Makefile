test:
	py.test --cov=llamedl tests/

test_e2e:
	py.test --cov=llamedl tests/e2e/e2e*

lint:
	black .

dev:
	pip install -r requirements/requirements-dev.txt