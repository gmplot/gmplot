
.PHONY: test

all: 
	@echo 'Nothing to make. Only "make test" works.'

test:
	coverage run -m unittest discover -v
