# Make sure to have pydoc-markdown:develop installed
# pip install git+https://github.com/NiklasRosenstein/pydoc-markdown.git@develop

# Script to make documentation
mkdir -p docs
mkdir -p docs/modules

rm -fr docs/*
pydoc-markdown pydoc-markdown.yaml -m whatstk >> docs/index.md

# mkdir -p docs/modules
# rm -fr docs/modules/*
# pydoc-markdown pydoc-markdown.yaml -m whatstk.objects >> docs/modules/whatstk.objects.md
# pydoc-markdown pydoc-markdown.yaml -m whatstk.plot >> docs/modules/whatstk.plot.md
# pydoc-markdown pydoc-markdown.yaml -m whatstk.analysis >> docs/modules/whatstk.analysis.md
# pydoc-markdown pydoc-markdown.yaml -m whatstk.utils >> docs/modules/whatstk.utils.md


