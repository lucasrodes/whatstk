Changelog
=========


v0.9.1
------

A parsing fix, plus dependency updates.

- **Bug fix**: Automatic header detection no longer depends on the chat spanning day 28. The day
  position was found by looking for a column whose maximum fell between 28 and 31; on a shorter
  chat nothing matched and the first column was used instead. Measured over the 96 supported
  formats on a chat confined to days 1–20, only 24 were detected correctly. The rest either parsed
  to the wrong dates with no error — ``2016-08-15`` read as ``2015-08-16`` — or raised an uncaught
  ``ValueError`` from ``datetime``. Day, month and year are now chosen by scoring every ordering
  against the values actually present, which detects all 96 at spans from two days to two years
  (#175).
- **Bug fix**: The ``llms.txt`` link on the documentation landing page pointed at a URL that
  returned 404.
- **Dependencies**: Updated ``anyio``, ``httplib2``, ``pyasn1`` and ``urllib3``.

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.9.0..HEAD

v0.9.0
------

The parser release. Five externally reported security issues fixed, several silent
data-loss bugs found and closed, and pandas 3 support.

.. warning::

    Two changes can require action:

    - **Inputs are now size-capped.** ``df_from_whatsapp`` refuses a chat whose text exceeds 50 MB.
      Pass ``max_size`` to raise the limit, or ``None`` to disable it. Roughly half a million
      messages, so it should not affect a real export.
    - **Dependency floors raised** to numpy 2.3.2 and pandas 2.3.3. The previous floors had no
      wheels for the newer Python versions.

- **Security**: Fixed a denial of service where a separator that is a regex metacharacter turned
  the header pattern exponential — a 173 byte chat could occupy the parser for hours, with no
  ``hformat`` supplied by the caller. Separators such as ``(``, ``*`` and ``|`` also raised
  uncaught ``re.PatternError`` and ``TypeError``. Literals are now escaped (report #1799).
- **Security**: The ZIP loader no longer extracts to disk and no longer reads without a limit. A
  59 KB archive could expand to 265 MB of memory; over-limit archives are now refused before
  anything is decompressed (report #1800).
- **Security**: Google Drive credentials are written ``0600`` inside a ``0700`` directory. The
  client secret had been world-readable, and a file the user had protected was silently widened
  when copied (report #1611).
- **Security**: Sample chat URLs use HTTPS (report #1814).
- **Bug fix**: Merging chats no longer discards messages. Chats were ordered by a sort that did
  nothing, and messages falling inside a range already covered were dropped — merging two exports
  of one conversation lost 6 of 21 messages. Merging now returns the deduplicated union, ordered by
  date (report #1872).
- **Bug fix**: A chat whose first header differs in shape from the rest no longer decides the
  format for the whole file, which could produce a malformed format and an uncaught
  ``re.PatternError`` (#175).
- **Bug fix**: ``extract_header_from_text`` returns a format that can be passed straight back as
  ``hformat``. Bracketed iOS-style formats were returned pre-escaped and crashed on reuse.
- **Bug fix**: ``rename_users`` used chained assignment, which pandas copy-on-write discards. On
  pandas 3 it would have returned an unchanged chat.
- **Unicode**: Normalisation uses NFKC instead of NFKD, so accented characters stay composed, and
  ZWJ/ZWNJ are preserved so compound emoji and Persian text survive (#171, #172).
- **pandas 3.0 support**: Resolves pandas 2.3.3 through 3.1 (#170). A CI job now tests the oldest
  versions the pins allow, on the oldest and newest supported Python.
- **Deprecation**: Google Drive support warns and will be removed in 0.10.0. Download the export
  and pass a local path instead (#177).
- **Deprecation**: ``df_from_txt_whatsapp`` is no longer exported at the top level; import it from
  ``whatstk.whatsapp.parser``.
- **Documentation**: New pages on automatic header detection and on what whatstk cannot tell you —
  notably that the ``username`` column reports who an export *says* sent a message, which an export
  cannot prove. Added ``llms.txt`` for AI assistants, and ``AGENTS.md`` for contributors.
- **Typing**: pyright runs in standard mode with 20 previously disabled checks re-enabled.

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.8.1..HEAD


v0.8.1
------

A documentation and packaging release. No library code changed.

- **Documentation links**: Point at ``/en/latest/`` rather than ``/en/stable/`` throughout the
  README, the project metadata and the Read the Docs config, so links resolve to the current build.
- **Packaging**: Dropped the ``Development Status :: 4 - Beta`` and redundant
  ``Programming Language :: Python`` classifiers from ``pyproject.toml``.
- **README**: Pinned the PyPI badge to the released version instead of resolving it dynamically.

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: v0.8.0..v0.8.1

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
