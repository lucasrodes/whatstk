"""Load sample chat."""
# pip install --upgrade certifi


import os
from collections import namedtuple


Urls = namedtuple('Urls', ['pokemon', 'lorem'])

chats_folder = 'http://raw.githubusercontent.com/lucasrodes/whatstk/master/chats'

whatsapp_urls = Urls(
    pokemon=os.path.join(chats_folder, 'whatsapp', 'pokemon.txt'),
    lorem=os.path.join(chats_folder, 'whatsapp', 'lorem.txt')
)
