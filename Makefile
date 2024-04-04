.PHONY: all
all: build test

.PHONY: build
build:
	python3 -m build --sdist --wheel

.PHONY: clean
clean:
	rm -rf build dist
	rm -rf .tox .pytest_cache 

.PHONY: dist-clean
dist-clean:
	rm -rf lib/fakelab.egg-info

.PHONY: test
test:
	tox
