"""Generate multiple graphics for your chat using plotly."""


import argparse
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.graph import plot, FigureBuilder


def _parse_args():
    parser = argparse.ArgumentParser(description="Visualise a WhatsApp chat. For advance settings, see package library"
                                     "documentation")
    parser.add_argument(
        "input_filename", type=str, default=None, help="Input txt file."
    )
    parser.add_argument(
        "-o", "--output_filename", type=str, default="output.html", help="Graph generated can be stored as an HTML"
        "file."
    )
    parser.add_argument(
        "-t", "--type", type=str, default="interventions_count",
        choices=['interventions_count', 'msg_length'],
        help="Type of graph."
    )
    parser.add_argument(
        "-id", "--icount-date-mode", type=str, default="date", choices=["date", "hour", "weekday", "month"],
        help="Select date mode. Only valid for --type=interventions_count."
    )
    parser.add_argument(
        "-ic", "--icount-cummulative", action="store_true",
        help="Show values in a cummulative fashion. Only valid for --type=interventions_count."
    )
    parser.add_argument(
        "-il", "--icount-msg-length", action="store_true",
        help="Count an intervention with its number of characters. Otherwise an intervention is count as one."
        "Only valid for --type=interventions_count."
    )
    parser.add_argument(
        '-f', "--hformat", type=str, default=None, help="By default, auto-header detection is"
        "attempted. If does not work, you can specify it manually using this argument."
    )
    args = parser.parse_args()
    return args


def main():
    """Main script."""
    args = _parse_args()
    chat = WhatsAppChat.from_source(filepath=args.input_filename, hformat=args.hformat)

    if args.type == "interventions_count":
        fig = FigureBuilder(
            chat=chat
        ).user_interventions_count_linechart(
            date_mode=args.icount_date_mode,
            msg_length=False,
            cummulative=args.icount_cummulative
        )
    elif args.type == "msg_length":
        fig = FigureBuilder(
            chat=chat
        ).user_msg_length_boxplot()
    plot(fig, filename=args.output_filename)
