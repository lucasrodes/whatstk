from whatstk.plot import vis
from whatstk.objects import WhatsAppChat
from whatstk.analysis import interventions
import os


filenames_path = "./tests/chats"
filenames = [os.path.join(filenames_path, f) for f in os.listdir(filenames_path) if f.endswith(".txt")]


def test_vis():
    for filename in filenames:
        chat = WhatsAppChat.from_txt(filename)
        counts = interventions(chat=chat, date_mode='date', msg_length=False)
        counts_cumsum = counts.cumsum() 
        fig = vis(counts_cumsum, 'cumulative number of messages sent per day')
        assert isinstance(fig, dict)
        assert ('data' in fig and 'layout' in fig)
