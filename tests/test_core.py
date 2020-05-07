import os
from whatstk.core import df_from_txt


filenames_path = "./tests/chats"
filenames = [os.path.join(filenames_path, f) for f in os.listdir(filenames_path) if f.endswith(".txt")]


def test_df_from_txt():
    filename = os.path.join(filenames_path, 'example_1.txt')
    # Auto
    chat = df_from_txt(filename)