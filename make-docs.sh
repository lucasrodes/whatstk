# Script to make documentation
mkdir -p docs

pydoc-markdown -m whatstk.objects >> docs/whatstk.objects.md
pydoc-markdown -m whatstk.plot >> docs/whatstk.plot.md
pydoc-markdown -m whatstk.analysis >> docs/whatstk.analysis.md
pydoc-markdown -m whatstk.utils >> docs/whatstk.utils.md