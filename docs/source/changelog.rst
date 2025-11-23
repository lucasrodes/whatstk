Changelog
=========

Unreleased
----------

.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: v0.7.1..HEAD

v0.7.1
------
**Bugfix and robustness release** on top of **v0.7.0**.

- **Text cleaning is now more robust**, improving handling of **Unicode and special characters** in chats.
- **ZIP support is expanded and stabilised**: you can **read chats directly from ZIP archives** and **export with explicit encoding** via ``to_zip``.
- The library now **uses system messages** more consistently in the interface, improving clarity and UX.
- **CI/CD and documentation** have been refreshed: fixed Travis badge links, **pinned doc dependencies** (working around a docutils/RtD bullet rendering issue), and cleaned up links and examples.
- **Dependency updates and typing cleanups** (e.g. bumping ``scipy`` and ignoring selected static-analysis warnings) keep the project aligned with modern tooling.
- **Python 3.8 support is deprecated**, and legacy pieces like the old ``webapp.py`` and Gitter integration have been removed/deprecated to simplify maintenance.


.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: v0.6.3..v0.7.1

v0.6.3
------
**Maintenance release** that **updates dependencies** (including ``certifi``) and **aligns CI with Python 3.10 and 3.11 support** while dropping 3.7. Improves **documentation and links** (including chat/demo and Read the Docs config) and performs minor **linting and typing cleanups** to keep the project stable on modern environments.


.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: v0.5.0..v0.6.3

v0.5.0
------
**Adds Google Drive support** for loading chats, brings **official Windows compatibility** (paths, encoding, wheels), and **reorganises dependencies/extras** to make installing the “full” library easier. Documentation, Travis CI config, and project links are refreshed, and the deprecated **``cummulative`` argument is phased out** with minor cleanups and tests.


.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: v0.4.1..v0.5.0

v0.4.1
------
Patch on top of the 0.4 line that **lets you export to CSV without the index column**, applies a small **bug fix and dependency updates**, and polishes the **documentation and project metadata** (Read the Docs links, badges, funding info). The broader 0.4.x series also brings **Python 3.9 support**, a **cleaner DataFrame structure** (numeric index + date column), and a refreshed **contribution/docs experience**.

.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: v0.3.1..v0.4.1

v0.3.1
------
Patch release on top of v0.3.0 that **cleans up the API and messaging around header auto-detection** (more verbose `HFormatError` pointing users to GitHub issues) and **fixes the deprecated `cummulative` variable/typo**, while the broader v0.3 line introduces **rich interactive visualisations** (Plotly/graph module, response matrix & Sankey diagrams, CLI tools for graphs and txt→csv), **more flexible chat import/export** (merge multiple chats, `df_from_txt` / `df_from_multiple_txt`, dataframe support, robust auto-header for many formats), and a **large documentation + CI overhaul** (Sphinx docs, sample chats, Travis + coverage + automated deployment).


.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: v0.2.6..v0.3.1

v0.2.6
------
**Improves header handling** with auto-detection and full support for **12-hour WhatsApp chat headers**, backed by new tests and example chats. Refines the **documentation and public-facing materials** (README refactor, security notes, GUI app link, badges) and stabilises the **CI/release pipeline** with Travis, Codecov integration, and **pandas compatibility fixes** (`argmax`/`argmin` → `idxmax`/`idxmin`).


.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: 0.1.11..v0.2.6

v0.1.11
-------
Early stable release that solidifies the core WhatsApp chat parsing and visualization toolkit: adds support for more date/header formats (including 2-digit years), improves performance and plotting (weekly activity grids, response matrices, SOM-based similarity, violin plots), and refreshes notebooks, docs, and examples. Packaging and CI are set up for installation via pip (PyPI), with clearer dependencies and Python 2.7 / 3.x compatibility.

.. container:: toggle

    .. container:: header

        **Show all commits**

    .. git_changelog::
        :rev-list: 0.1.10

