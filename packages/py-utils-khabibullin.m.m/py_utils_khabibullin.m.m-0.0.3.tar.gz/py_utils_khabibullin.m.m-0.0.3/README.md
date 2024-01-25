# Example
https://github.com/pypa/sampleproject
https://packaging.python.org/en/latest/tutorials/packaging-projects/

# Example Package

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

# DEPLOY
Update version
Remove "dist" folder
py -m build
py -m twine upload --repository testpypi dist/*

# INSTALL
pip install py-utils-khabibullin.m.m --index-url https://test.pypi.org/simple/
