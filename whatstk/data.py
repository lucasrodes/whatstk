"""Load sample chats.

The objective of this module is to have the links to currently online-available chats. For more details, please refer to
the source code.
"""
# pip install --upgrade certifi


import os
from collections import namedtuple


Urls = namedtuple('Urls', [
    'POKEMON',
    'LOREM'
])

branch = 'develop'
chats_folder = f'http://raw.githubusercontent.com/lucasrodes/whatstk/{branch}/chats'

whatsapp_urls = Urls(
    POKEMON=os.path.join(chats_folder, 'whatsapp', 'pokemon.txt'),
    LOREM=os.path.join(chats_folder, 'whatsapp', 'lorem.txt')
)
