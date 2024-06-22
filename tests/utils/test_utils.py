from whatstk.utils.utils import COLNAMES_DF

def test_colnames():
    assert COLNAMES_DF.DATE == "date"
    assert COLNAMES_DF.USERNAME == "username"
    assert COLNAMES_DF.MESSAGE == "message"
    assert COLNAMES_DF.MESSAGE_LENGTH == "message_length"
    assert COLNAMES_DF.MESSAGE_TYPE == "message_type"
