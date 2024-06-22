from whatstk.whatsapp.auto_header import extract_header_from_text, _extract_elements_template_from_lines


def test_extract_header_from_text():
    _ = extract_header_from_text("bla bla bla")
    assert _ is None


def test_extract_elements_template_from_lines():
    elements_list, template_list = _extract_elements_template_from_lines(["testing"])
    assert elements_list == []
    assert template_list == []


