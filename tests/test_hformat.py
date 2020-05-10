from whatstk.utils.hformat import is_supported, is_supported_verbose, get_supported_hformats_as_list


def test_is_supported_1():
    hformat = '%Y-%m-%d, %H:%M - %name:'
    support, autoh_support = is_supported(hformat)
    assert(isinstance(support, bool))
    assert(isinstance(autoh_support, bool))


def test_is_supported_2():
    hformat = '%Y-%m-%d, %I:%M %P - %name:'
    support, autoh_support = is_supported(hformat)
    assert(isinstance(support, bool))
    assert(isinstance(autoh_support, bool))


def test_is_supported_verbose():
    hformat = '%Y-%m-%d, %I:%M %P - %name:'
    support_msg = is_supported_verbose(hformat)
    assert(isinstance(support_msg, str))


def test_get_supported_hformats_as_list():
    supported_headers = get_supported_hformats_as_list()
    assert(isinstance(supported_headers, list))
    assert(all([isinstance(h, str) for h in supported_headers]))
