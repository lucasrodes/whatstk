"""Generate chats in all hformats with `size` number of messages and export them to a given `output_path`."""
import argparse
from whatstk.objects import WhatsAppChat


def _parse_args():
    parser = argparse.ArgumentParser(description="Convert a Whatsapp chat from csv to txt.")
    parser.add_argument("input_filename", default=None, help="Input txt file.", type=str)
    parser.add_argument("output_filename", help="Name of output csv file.", type=str)
    parser.add_argument("--hformat", help="By default, auto-header detection is attempted. If does not work, you can"
                        "specify it manually using this argument.", type=str)
    args = parser.parse_args()
    return args


def main():
    """Main script."""
    args = _parse_args()
    chat = WhatsAppChat.from_txt(filename=args.input_filename)
    chat.to_csv(args.output_filename)
