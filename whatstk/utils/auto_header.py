"""Detect header from chat."""


import logging
import re
import pandas as pd
from whatstk.utils.exceptions import RegexError


separators = {'.', ',', '-', '/', ':', '[', ']'}


def extract_header_from_text(text, encoding='utf-8'):
    """Extract header from filename.

    Args:
        text (str): Loaded chat as string (whole text).
        encoding (str, optional): Encoding to be used. Defaults to 'utf-8'.

    Returns:
        str: Format extracted. None if no header was extracted.

    """
    # Split lines
    lines = text.split('\n')

    # Get format auto
    try:
        hformat = extract_header_format_from_lines(lines)
        logging.info("Format found was %s", hformat)
        return hformat
    except:  # noqa
        logging.info("Format not found.")
    return None


# def issep(s):
#     """Check if `s` is a separator character.

#     Separator can be one of the following: '.', ',', '-', '/', ':', '[' or ']'.

#     Args:
#         s (str): Character to be checked.

#     Returns:
#         bool: True if `s` is a separator, False otherwise.

#     """
#     if s in separators:
#         return True
#     return False


def extract_header_format_from_lines(lines):
    """Extract header from list of lines.

    Args:
        lines (list): List of str, each element is a line of the loaded chat.

    Returns:
        str: Format of the header.

    """
    # Obtain header format from list of lines
    elements_list, template_list = _extract_elements_template_from_lines(lines)
    return _extract_header_format_from_components(elements_list, template_list)


def _extract_elements_template_from_lines(lines):
    """Get elements_list and template_list from lines.

    Args:
        lines (list): List with messages.

    Returns:
        tuple: elements_list (list), template_list (list)
    """
    # Obtain header format from list of lines
    elements_list = []
    template_list = []
    for line in lines:
        header = _extract_possible_header_from_line(line)
        if header:
            try:
                elements, template = _extract_header_parts(header)
            except RegexError:
                continue
            elements_list.append(elements)
            template_list.append(template)
    return elements_list, template_list


def _extract_possible_header_from_line(line):
    """Given a `line` extract possible header. Uses ':' as separator.

    Args:
        line (str): Line containing header and message body.

    Returns:
        str: Possible header.

    """
    # Extract possible header from line
    line_split = line.split(': ')
    if len(line_split) >= 2:
        # possible header
        header = line_split[0]
        if not header.isprintable():
            header = header.replace('\u200e', '').replace('\u202e', '')
        if header[-1] != ':':
            header += ':'
        return header
    return None


def _extract_header_parts(header):
    """Extract all parts from header (i.e. date elements and name).

    Args:
        header (str): Header.

    Returns:
        tuple: Contains two elements, (i) list with components and (ii) string template which specifies the formatting
                of the components.
    """

    def get_last_idx_digit(v, i):
        if i+1 < len(v):
            if v[i+1].isdigit():
                return get_last_idx_digit(v, i+1)
        return i

    # def get_last_idx_alpha(v, i):
    #     if i+1 < len(v):
    #         if v[i+1].isalpha():
    #             return get_last_idx_alpha(v, i+1)
    #         elif i+2 < len(v):
    #             if v[i+1].isspace() and v[i+2].isalpha():
    #                 return get_last_idx_alpha(v, i+2)
    #     return i

    hformat_elements = []
    hformat_template = ''
    i = 0
    while i < len(header):
        if header[i].isdigit():
            j = get_last_idx_digit(header, i)
            hformat_elements.append(int(header[i:j+1]))
            hformat_template += '{}'
            i = j
        else:
            if header[i] in ['[', ']']:
                hformat_template += '\\'+header[i]
            else:
                hformat_template += header[i]
        i += 1
    items = re.findall(r'[-|\]]\s[^:]*:', hformat_template)
    if len(items) != 1:
        raise RegexError(
            "Username match was not possible. Check that header (%s) is of format '... - %name:' or '[...] %name:'",
            hformat_template)
    hformat_template = hformat_template.replace(items[0][2:-1], '%name')
    code = ' %p'
    hformat_template = hformat_template\
        .replace(' PM', code)\
        .replace(' AM', code)\
        .replace(' A.M.', code)\
        .replace(' P.M.', code)\
        .replace(' am', code)\
        .replace(' pm', code)\
        .replace(' a.m.', code)\
        .replace(' p.m.', code)
    return hformat_elements, hformat_template


def _extract_header_format_from_components(elements_list, template_list):
    """Extract header format from list containing elements and list containing templates.

    Args:
        elements_list (list): List with component list.
        template_list (list): List with template strings.

    Returns:
        str: Header format.

    """
    # Remove outliers
    elements_list_ = []
    template_list_ = []
    lengths = [len(e) for e in elements_list]
    types = ["".join([str(type(ee).__name__) for ee in e]) for e in elements_list]
    len_mode = max(set(lengths), key=lengths.count)
    type_mode = max(set(types), key=types.count)
    for e, t in zip(elements_list, template_list):
        if (len(e) == len_mode) and ("".join([str(type(ee).__name__) for ee in e]) == type_mode):
            elements_list_.append(e)
            template_list_.append(t)
    # Get positions
    df = pd.DataFrame(elements_list_)
    dates_df = df.select_dtypes(int)

    template = template_list[0]

    if '%p' in template:
        hour_code = "%I"
    else:
        hour_code = "%H"

    # day
    day_pos = ((dates_df.max() > 27) & (dates_df.max() < 32)).idxmax()
    dates_df = dates_df.drop(columns=[day_pos])
    # year
    # year_pos = dates_df.std().idxmin()
    pos = [0, 1, 2]
    pos.remove(day_pos)
    year_pos = dates_df[pos].max().idxmax()  # Only consider positions 0,1,2
    dates_df = dates_df.drop(columns=[year_pos])
    # Month
    month_pos = dates_df.columns.min()
    dates_df = dates_df.drop(columns=[month_pos])
    # Hour
    hour_pos = 3
    dates_df = dates_df.drop(columns=[hour_pos])
    # Minute
    minutes_pos = 4
    dates_df = dates_df.drop(columns=[minutes_pos])
    # Dictionary with positions and date element code
    dates_pos = {
        day_pos: '%d',
        year_pos: '%y',
        month_pos: '%m',
        hour_pos: hour_code,
        minutes_pos: '%M'
    }
    # Seconds
    if dates_df.shape[1] > 0:
        seconds_pos = 5
        dates_pos[seconds_pos] = '%S'

    keys_ordered = sorted(dates_pos.keys())
    dates_codes = [dates_pos[k] for k in keys_ordered]

    codes = dates_codes + ['%name']
    # print(codes)
    # print(template)
    # print(template)
    # print(codes)
    code_template = template.format(*codes)
    # print(code_template)
    # print('---------------')
    # print(code_template)
    return code_template
