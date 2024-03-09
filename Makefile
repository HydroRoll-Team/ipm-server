PYTHON = python
BASEURL = https://raw.githubusercontent.com/HydroRoll-Team/ipm-server/gh-pages/packages

pkg_index:
	$(PYTHON) tools/build_collections.py .
	$(PYTHON) tools/build_pkg_index.py . $(BASEURL) index.xml

grammars:
	git commit -m "updated grammar files" packages/grammars