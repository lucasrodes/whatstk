# Make sure to have pydoc-markdown:develop installed
# pip install git+https://github.com/NiklasRosenstein/pydoc-markdown.git@develop

# Script to make documentation
mkdir -p docs

rm -fr docs/*
pydoc-markdown pydoc-markdown.yaml -m whatstk.objects >> docs/whatstk.objects.md
pydoc-markdown pydoc-markdown.yaml -m whatstk.plot >> docs/whatstk.plot.md
pydoc-markdown pydoc-markdown.yaml -m whatstk.analysis >> docs/whatstk.analysis.md
pydoc-markdown pydoc-markdown.yaml -m whatstk.utils >> docs/whatstk.utils.md