"""Generate chats in all hformats with `size` number of messages and export them to a given `output_path`."""


import argparse
from whatstk.whatsapp.objects import WhatsAppChat


def _parse_args() -> None:
    parser = argparse.ArgumentParser(description="Convert a Whatsapp chat from csv to txt.")
    parser.add_argument("input_filename", type=str, help="Input txt file.")
    parser.add_argument("output_filename", type=str, help="Name of output csv file.")
    parser.add_argument(
        "-f",
        "--hformat",
        type=str,
        default=None,
        help="By default, auto-header detection is"
        "attempted. If does not work, you can specify it manually using this argument.",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    """Main script."""
    args = _parse_args()
    chat = WhatsAppChat.from_source(filepath=args.input_filename, hformat=args.hformat)
    chat.to_csv(args.output_filename)
