# Contributing to WPyDumps

## Release a new version

Ensure you have up-to-date distributing tools:

    python3 -m pip install --upgrade pip setuptools wheel twine

Then:

1. Update the Changelog
2. Bump the version in `wpydumps/__init__.py`
3. Commit and tag
4. `rm -rf dist/*`
5. `python3 setup.py sdist bdist_wheel`
6. `twine check dist/*`
7. `twine upload dist/*`

[More info here](https://packaging.python.org/tutorials/packaging-projects/).
