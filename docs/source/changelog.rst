Changelog
=========


v0.8.0
----------

- **Python version support**: Added Python 3.13 and 3.14 support, dropped Python 3.9 and 3.10
- **Build system**: Migrated to ``uv`` for dependency management and build process
- **CI improvements**: Migrated from Travis CI to GitHub Actions, added matrix builds
- **Testing**: Added ``pytest-xdist`` for parallel testing and improved test suite
- **Documentation**: Updated contribution guidelines, README, and removed Gitter references
- **Bug fixes**: Fixed issue #61 and other minor bugs
- **Code quality**: Added ``pyright`` configuration and applied formatting improvements

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.7.1..HEAD

v0.7.1
------

- **Dependency updates**: Updated ``scipy``, ``pandas``, and ``certifi`` to latest versions
- **Python 3.13 support**: Made project ready for Python 3.13
- **CI improvements**: Enhanced continuous integration pipeline
- **Documentation improvements**: Improved contribution documentation
- **Code cleanup**: Removed Gitter references and applied formatting improvements
- **Security**: Keep dependencies modern and secure


.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.6.3..v0.7.1

v0.6.3
------

- **Python version support**: Added Python 3.10 and 3.11, dropped Python 3.7
- **Dependency updates**: Updated dependencies including ``certifi``
- **CI alignment**: Updated continuous integration for new Python versions
- **Documentation**: Improved links, chat/demo references, and Read the Docs config
- **Code quality**: Linting and typing cleanups


.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.5.0..v0.6.3

v0.5.0
------

- **Google Drive support**: Load chats directly from Google Drive
- **Windows compatibility**: Official support for Windows (paths, encoding, wheels)
- **Dependencies reorganization**: Easier installation with reorganized extras
- **Deprecated argument removal**: Phased out ``cumulative`` typo argument
- **Documentation updates**: Refreshed Travis CI config and project links
- **Code cleanup**: Minor cleanups and additional tests


.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.4.1..v0.5.0

v0.4.1
------

- **CSV export improvement**: Export to CSV without index column
- **Python 3.9 support**: Added support for Python 3.9
- **DataFrame structure**: Cleaner structure with numeric index and date column
- **Bug fixes**: Small bug fixes and dependency updates
- **Documentation**: Polished metadata, Read the Docs links, badges, and funding info
- **Contribution experience**: Refreshed contribution and docs experience

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.3.1..v0.4.1

v0.3.1
------

- **Plotly integration**: Visualizations now use Plotly by default
- **New plot types**: Added Sankey diagrams and violin plots
- **rename_users() method**: Consolidate user names in merged chats
- **Cumulative charts**: New cumulative chart functionality
- **DataFrame improvements**: Added dedicated date column for easier manipulation
- **Command-line tools**: Enhanced chat-gen with new arguments
- **Documentation**: Updated examples and documentation


.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.2.6..v0.3.1

v0.2.6
------

- **12-hour format support**: Full support for 12-hour WhatsApp chat headers
- **Header auto-detection**: Improved header handling with auto-detection
- **Pandas compatibility**: Fixed compatibility issues (`argmax`/`argmin` → `idxmax`/`idxmin`)
- **CI/release pipeline**: Stabilized with Travis and Codecov integration
- **Documentation**: Refactored README, added security notes and GUI app link
- **Testing**: Added new tests and example chats


.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: 0.1.11..v0.2.6

v0.1.11
-------

- **Date format support**: Added support for more formats including 2-digit years
- **Visualization improvements**: Weekly activity grids, response matrices, violin plots
- **SOM-based similarity**: New similarity analysis features
- **PyPI packaging**: Set up for installation via pip
- **Python compatibility**: Support for Python 2.7 and 3.x
- **Documentation**: Refreshed notebooks, docs, and examples
- **Performance**: Various performance improvements

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: 0.1.10
