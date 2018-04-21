
.PHONY: test

all: 
	@echo 'Nothing to make. Only "make test" works.'

test:
	python -m unittest discover -v
