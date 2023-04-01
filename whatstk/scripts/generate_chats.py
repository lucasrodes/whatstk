"""Generate chats in all hformats with `size` number of messages and export them to a given `output_path`."""


import argparse
from datetime import datetime
from whatstk.whatsapp.generation import generate_chats_hformats


def _parse_args() -> None:
    parser = argparse.ArgumentParser(
        "Generate chat. Make sure to install the library with required extension: pip install whatstk[generate] "
        "--upgrade"
    )
    parser.add_argument(
        "-o", "--output-path", type=str, required=True, help=("Path where to store generated chats. Must exist.")
    )
    parser.add_argument("--filenames", default=None, nargs="+", help="Filenames. Must be equal length of --hformats.")
    parser.add_argument(
        "-s", "--size", type=int, default=500, help="Number of messages to create per chat. Defaults to 500."
    )
    parser.add_argument(
        "-f",
        "--hformats",
        default=None,
        nargs="+",
        help="Header format. If None, defaults to all supported hformats. List formats as 'format 1' 'format 2' ...",
    )
    parser.add_argument(
        "--last-timestamp",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=None,
        help="Timestamp of last message. Format YYYY-mm-dd",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity.")
    args = parser.parse_args()
    return args


def main() -> None:
    """Main script."""
    args = _parse_args()
    generate_chats_hformats(
        output_path=args.output_path,
        size=args.size,
        hformats=args.hformats,
        last_timestamp=args.last_timestamp,
        filepaths=args.filenames,
    )
