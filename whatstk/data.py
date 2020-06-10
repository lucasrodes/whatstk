"""Load sample chat."""
# pip install --upgrade certifi


import os
from collections import namedtuple


Urls = namedtuple('Urls', ['pokemon', 'lorem'])

branch = 'develop'
chats_folder = f'http://raw.githubusercontent.com/lucasrodes/whatstk/{branch}/chats'

whatsapp_urls = Urls(
    pokemon=os.path.join(chats_folder, 'whatsapp', 'pokemon.txt'),
    lorem=os.path.join(chats_folder, 'whatsapp', 'lorem.txt')
)
