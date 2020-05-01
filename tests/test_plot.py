from whatstk.plot import vis
from whatstk.objects import WhatsAppChat
from whatstk.analysis import interventions


def test_vis():
    filename = 'tests/chats/example_1.txt'
    chat = WhatsAppChat.from_txt(filename)
    counts = interventions(chat=chat, date_mode='date', msg_length=False)
    counts_cumsum = counts.cumsum() 
    fig = vis(counts_cumsum, 'cumulative number of messages sent per day')
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)
