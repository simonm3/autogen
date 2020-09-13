# Minimal makefile for Sphinx documentation
#
.PHONY:  default clean rst html

all:
	make clean rst html

# close existing output
clean:
	rm -rf _rst
	rm -rf _build

# create directives for docstrings in docs/_rst/*.rst
rst:
	sphinx-apidoc -o _rst .. ../*/test ../*/examples ../*/ipstartup.py ../setup.py
	python clean_rst.py

# create html
html:
	sphinx-build -M html . _build -b coverage 

