import pytest

from whatstk.data import whatsapp_urls


def test_urls():
    url = whatsapp_urls.POKEMON
    assert isinstance(url, str)
    assert url.startswith("http")


def test_sample_chat_urls_use_https():
    """Sample chats must be fetched over TLS.

    Report #1814: these URLs used http://. GitHub redirects to https, but the first request still
    travels in the clear, so a network attacker can answer before the redirect and serve a chat of
    their choosing.
    """
    for name, url in whatsapp_urls._asdict().items():
        assert url.startswith("https://"), f"{name} is not https: {url}"


def test_deprecated_alias_is_not_exported_at_top_level():
    """`df_from_txt_whatsapp` is deprecated; it stays importable from its own module only."""
    import whatstk

    assert "df_from_txt_whatsapp" not in whatstk.__all__
    assert not hasattr(whatstk, "df_from_txt_whatsapp")

    from whatstk.whatsapp.parser import df_from_txt_whatsapp  # still importable

    assert callable(df_from_txt_whatsapp)


def test_figurebuilder_is_resolved_lazily():
    """`import whatstk` must not pull in plotly.

    Plotting sits behind the `viz` extra, so FigureBuilder is resolved on first attribute access
    rather than at import time. Without this, installing whatstk to parse a chat would still
    require plotly and seaborn.
    """
    import whatstk

    assert "FigureBuilder" in whatstk.__all__
    # Resolvable here because the dev environment installs [viz].
    assert whatstk.FigureBuilder is not None

    with pytest.raises(AttributeError, match="has no attribute"):
        _ = whatstk.NotAThing
