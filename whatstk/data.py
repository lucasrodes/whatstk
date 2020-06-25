"""Load sample chats.

Tthis module contains the links to currently online-available chats. For more details, please refer
to the source code.

"""
# pip install --upgrade certifi


import os
from collections import namedtuple


Urls = namedtuple('Urls', [
    'POKEMON',
    'LOREM',
    'LOREM1',
    'LOREM2',
    'LOREM_2000'
])

branch = 'develop'
chats_folder = f'http://raw.githubusercontent.com/lucasrodes/whatstk/{branch}/chats'

whatsapp_urls = Urls(
    POKEMON=os.path.join(chats_folder, 'whatsapp', 'pokemon.txt'),
    LOREM=os.path.join(chats_folder, 'whatsapp', 'lorem.txt'),
    LOREM1=os.path.join(chats_folder, 'whatsapp', 'lorem-merge-part1.txt'),
    LOREM2=os.path.join(chats_folder, 'whatsapp', 'lorem-merge-part2.txt'),
    LOREM_2000=os.path.join(chats_folder, 'whatsapp', 'lorem-2000.txt')
)
