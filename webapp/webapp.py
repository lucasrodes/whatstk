"""
# My first app
Here's our first attempt at using data to create a table:
"""

from pathlib import Path
import streamlit as st
import tempfile
from whatstk import df_from_txt_whatsapp


# Page settings
st.set_page_config(
    page_title="WhatsApp chat parser",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Side bar
with st.sidebar:
    hformat = st.text_input(
        "Header format",
        help="More info at https://whatstk.readthedocs.io/en/stable/source/getting_started/hformat.html.",
    )
    encoding = st.text_input(
        "Encoding",
        value="utf-8",
        help="Encoding of the chat.",
    )

# Encoding default
ENCODING_DEFAULT = "utf-8"

# APP title
st.title('WhatsApp chart parser')


# Upload file box
uploaded_file = st.file_uploader(
    label="Upload a file",
    type="txt",
    label_visibility="collapsed",
)

# Define temporary file (chat will be stored here temporarily)
temp_dir = tempfile.TemporaryDirectory()
uploaded_file_path = Path(temp_dir.name) / "chat"

if uploaded_file is not None:
    with open(uploaded_file_path, 'wb') as output_temporary_file:
        output_temporary_file.write(uploaded_file.read())

    # Load file as dataframe
    try:
        df = df_from_txt_whatsapp(
            output_temporary_file.name,
            hformat=hformat,
            encoding=encoding,
        )
    except RuntimeError:
        st.error(
            "The chat could not be parsed automatically! You can try to set custom `hformat` "
            "value in the side bar config."
            "Additionally, please report to https://github.com/lucasrodes/whatstk/issues. If possible, "
            "please provide a sample of your chat (feel free to replace the actual messages with dummy text)."
        )
    else:
        # Download option
        csv = df.to_csv().encode(ENCODING_DEFAULT)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='chat.csv',
            mime='text/csv',
            help="Download the formatted chat as a CSV file",
        )

        # Print chat as dataframe
        with st.expander("Preview chat"):
            st.dataframe(df)
