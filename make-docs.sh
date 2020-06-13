# make documentation script

# 0. Install dependencies: # pip install -r requirements-docs.txt
# 1. sphinx-quickstart 
# 1b. select non split between source and html
# 2. add auto_doc in extensions:
# extensions = [
#     'sphinx.ext.autodoc'
# ]
# 3. use `$ make clean`
sphinx-apidoc -f -o source/ ../whatstk/ ['setup.py', 'tests/']
make html


# ref: https://opensource.com/article/19/11/document-python-sphinx
# ref: https://sphinx-themes.org/

# pip install -r requirements-docs.txt
# https://github.com/readthedocs/sphinx_rtd_theme