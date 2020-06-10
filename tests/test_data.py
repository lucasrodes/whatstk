from whatstk.data import whatsapp_urls


def test_urls():
    url = whatsapp_urls.pokemon
    assert(isinstance(url, str))
    assert(url.startswith('http'))
