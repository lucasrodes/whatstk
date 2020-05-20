from whatstk.plot import vis_scatter_time
from whatstk.objects import WhatsAppChat
from whatstk.analysis import interventions
import os


filename = "./tests/chats/hformats/[%d.%m.%y_%I:%M:%S_%p]_%name:.txt"


def test_vis_scatter_time():
    chat = WhatsAppChat.from_txt(filename)
    counts = interventions(chat=chat, date_mode='date', msg_length=False)
    counts_cumsum = counts.cumsum()
    fig = vis_scatter_time(counts_cumsum, 'cumulative number of messages sent per day')
    assert isinstance(fig, dict)
    assert ('data' in fig and 'layout' in fig)
