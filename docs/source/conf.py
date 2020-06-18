# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# # sys.path.insert(0, os.path.abspath('.'))
# sys.path.insert(0, os.path.abspath('_ext'))

from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary import get_documenter
from docutils.parsers.rst import directives
from sphinx.util.inspect import safe_getattr


# -- Project information -----------------------------------------------------

project = 'whatstk'
copyright = '2020, lucasrodes'
author = 'lucasrodes'

# The full version, including alpha/beta/rc tags
release = '0.3.0.dev1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
    'sphinx_git',
    'autodocsumm',
    'sphinx.ext.mathjax',
    # 'sphinx_multiversion'
    # 'sphinx_gallery.gen_gallery'
]

# The name of the entry point, without the ".rst" extension.
# By convention this will be "index"
master_doc = "content"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['../_build', '../Thumbs.db', '../.DS_Store', '../../../setup.py']
EXCLUDE_PATTERN = ['../../setup.py']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# html_theme = 'python_docs_theme'
# html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Copybutton ---------------------------------------------------------------
copybutton_prompt_text = ">>> "


# -- autoautosummary ----------------------------------------------------------
class AutoAutoSummary(Autosummary):
    option_spec = {
        'methods': directives.unchanged,
        'attributes': directives.unchanged
    }

    required_arguments = 1

    @staticmethod
    def get_members(obj, typ, include_public=None):
        if not include_public:
            include_public = []
        items = []
        for name in dir(obj):
            try:
                documenter = get_documenter(safe_getattr(obj, name), obj)
            except AttributeError:
                continue
            if documenter.objtype == typ:
                items.append(name)
        public = [x for x in items if x in include_public or not x.startswith('_')]
        return public, items

    def run(self):
        clazz = str(self.arguments[0])
        try:
            (module_name, class_name) = clazz.rsplit('.', 1)
            m = __import__(module_name, globals(), locals(), [class_name])
            c = getattr(m, class_name)
            if 'methods' in self.options:
                _, methods = self.get_members(c, 'method', ['__init__'])

                self.content = ["~%s.%s" % (clazz, method) for method in methods if not method.startswith('_')]
            if 'attributes' in self.options:
                _, attribs = self.get_members(c, 'attribute')
                self.content = ["~%s.%s" % (clazz, attrib) for attrib in attribs if not attrib.startswith('_')]
        finally:
            return super(AutoAutoSummary, self).run()

# -- Theme --------------------------------------------------------------------
def setup(app):
    app.add_stylesheet('css/custom.css')
    app.add_directive('autoautosummary', AutoAutoSummary)


html_title = "WhatsApp Analysis Toolkit"
html_logo = "../assets/logo.png"
html_favicon = "_static/favicon.png"

html_show_sourcelink = False
html_copy_source = True

# github_url = 'https://github.com/lucasrodes/whatstk'

html_theme_options = {
    'logo_only': True,
    'display_version': True,
    'navigation_depth': 3,
    'display_version': True,
    'collapse_navigation': False,
    'sticky_navigation': False
}

# -- Args ---------------------------------------------------------------------
html4_writer = True
napoleon_use_rtype = False
autosummary_generate = True


# Autodocsum
autodoc_default_options = {
    'autosummary': True,
}

# Sphinx gallery
# from plotly.io._sg_scraper import plotly_sg_scraper
# image_scrapers = ('matplotlib', plotly_sg_scraper,)

# sphinx_gallery_conf = {
#      'examples_dirs': '_static/examples_py',   # path to your example scripts
#      'gallery_dirs': 'source/gallery',  # path to where to save gallery generated output
#      'reference_url': {'plotly': None,
#       },
#      'image_scrapers': image_scrapers,
# }

# Github edit
edit_on_github_project = 'lucasrodes/whatstk'
edit_on_github_branch = 'master'
