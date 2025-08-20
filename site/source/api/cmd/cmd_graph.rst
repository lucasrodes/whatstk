``whatstk-graph``
=================

Get graph from your WhatsApp txt file.

.. code-block:: bash

    usage: whatstk-graph [-h] [-o OUTPUT_FILENAME]
                         [-t {interventions_count,msg_length}]
                         [-id {date,hour,weekday,month}] [-ic] [-il] [-f HFORMAT]
                         input_filename

    Visualise a WhatsApp chat. For advance settings, see package
    librarydocumentation

    positional arguments:
    input_filename        Input txt file.

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                            Graph generated can be stored as an HTMLfile.
    -t {interventions_count,msg_length}, --type {interventions_count,msg_length}
                            Type of graph.
    -id {date,hour,weekday,month}, --icount-date-mode {date,hour,weekday,month}
                            Select date mode. Only valid for
                            --type=interventions_count.
    -ic, --icount-cumulative
                            Show values in a cumulative fashion. Only valid for
                            --type=interventions_count.
    -il, --icount-msg-length
                            Count an intervention with its number of characters.
                            Otherwise an intervention is count as one.Only valid
                            for --type=interventions_count.
    -f HFORMAT, --hformat HFORMAT
                            By default, auto-header detection isattempted. If does
                            not work, you can specify it manually using this
                            argument.
