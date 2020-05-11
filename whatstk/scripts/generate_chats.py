"""Generate chats in all hformats with `size` number of messages and export them to a given `output_path`."""
import argparse
import ast
from datetime import datetime
from whatstk.utils.chat_generation import generate_chats_hformats


def _parse_args():
    parser = argparse.ArgumentParser()
    # For kubeflow
    # parser.add_argument("--output_path", help="Output path where the data should be saved.")
    parser.add_argument("--output-path", help="Path where to store generated chats. Must exist.", 
                            required=True, type=str)
    parser.add_argument("--filenames", default=None, help="Filenames. Must be equal length of --hformats.", 
                            nargs='+')
    parser.add_argument("--size", default=500, help="Number of messages to create per chat. Defaults to 500.", 
                            type=int)
    parser.add_argument("--hformats", default=None, help="Header format. If None, defaults to all supported hformats."
                                                         "List formats as 'format 1' 'format 2' ..." , nargs='+')
    parser.add_argument("--last-timestamp", default=None, help="Timestamp of last message. Format YYYY-mm-dd", 
                            type=lambda s: datetime.strptime(s, "%Y-%m-%d"))
    
    parser.add_argument("--verbose", action="store_true", help="Verbosity.")
    args = parser.parse_args()
    return args


def main():
    args = _parse_args()
    generate_chats_hformats(
        output_path=args.output_path, size=args.size, hformats=args.hformats, last_timestamp=args.last_timestamp,
        filenames=args.filenames
    )