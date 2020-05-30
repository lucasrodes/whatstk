from whatstk.plot import vis
from whatstk.objects import WhatsAppChat
from whatstk.analysis import get_interventions_count


filename = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_vis():
    chat = WhatsAppChat.from_txt(filename)
    counts = get_interventions_count(chat=chat, date_mode='date', msg_length=False)
    counts_cumsum = counts.cumsum()
    fig = vis(counts_cumsum, 'cumulative number of messages sent per day')
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)
