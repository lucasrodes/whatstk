import os
import pandas as pd
from whatstk.core import df_from_txt
from whatstk.utils.chat_generation import generate_chats_hformats
from whatstk.utils.hformat import get_supported_hformats_as_dict


# Generate chats
output_folder = "./tests/chats/hformats"
# generate_chats_hformats(output_folder, 500, verbose=True)
filenames = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.txt')]


def test_df_from_txt():
    """This test checks most of the logic of the library.

    - Generates tests in all formats to be supported (according to JSON)
    - Loads them using manual and auto_header approaches (checks they are equivalent).
    - Checks that all chats (from different hformats) are equivalent.

    """
    info_dix = get_supported_hformats_as_dict()
    all_chats = []
    hformats = []
    for elem in info_dix:
        chats = []
        hformat = elem['format']
        auto_header = bool(elem['auto_header'])
        filename = hformat.replace(' ', '_').replace('/', '\\')
        filename = os.path.join(output_folder, '{}.txt'.format(filename))

        # Auto
        if auto_header:
            chat = df_from_txt(filename)
            chats.append(chat)
        # Manual
        chat = df_from_txt(filename, hformat=hformat)
        chats.append(chat)

        # Check manual and auto chats are equal
        assert(chats[0].equals(chats[1]))
        
        all_chats.append(chat)
        hformats.append(hformat)
    
    records = []
    for i in range(len(all_chats)):
        record = {'chat': i}
        for j in range(i, len(all_chats)):
            if (all_chats[i].index.second.nunique() == 1) & (all_chats[j].index.second.nunique() != 1):
                all_chats[j].index = all_chats[j].index.map(lambda x: x.replace(second=0))
            elif (all_chats[j].index.second.nunique() == 1) & (all_chats[i].index.second.nunique() != 1):
                all_chats[i].index = all_chats[i].index.map(lambda x: x.replace(second=0))
            record[j] = all_chats[i].equals(all_chats[j])
        records.append(record)
    df = pd.DataFrame.from_records(records, index="chat")
    assert((df == False).sum().sum() == 0)