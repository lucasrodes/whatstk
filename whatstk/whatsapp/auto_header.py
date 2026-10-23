"""Detect header from chat."""

import itertools
import logging
import re
from typing import List, Tuple, Optional, cast
import pandas as pd

from whatstk.utils.exceptions import RegexError


separators = {".", ",", "-", "/", ":", "[", "]"}


def extract_header_from_text(text: str, encoding: str = "utf-8") -> Optional[str]:
    """Extract header from text.

    Args:
        text (str): Loaded chat as string (whole text).
        encoding (str): Encoding to use for UTF when reading/writing (ex. ‘utf-8’).
                             `List of Python standard encodings
                             <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

    Returns:
        str: Format extracted. None if no header was extracted.

    Example:
            Load a chat using two text files. In this example, we use sample chats (available online, see urls in
            source code :mod:`whatstk.data <whatstk.data>`).

            ..  code-block:: python

                >>> from whatstk.whatsapp.parser import extract_header_from_text
                >>> from urllib.request import urlopen
                >>> from whatstk.data import whatsapp_urls
                >>> filepath_1 = whatsapp_urls.POKEMON
                >>> with urlopen(filepath_1) as f:
                ...     text = f.read().decode('utf-8')
                >>> extract_header_from_text(text)
                '%d.%m.%y, %H:%M - %name:
    """
    # Split lines
    lines = text.split("\n")

    # Get format auto
    try:
        hformat = _extract_header_format_from_lines(lines)
        logging.info("Format found was %s", hformat)
        return hformat
    except Exception as err:  # noqa: BLE001 - detection is best-effort; the caller raises if it returns None
        logging.info("Format not found: %s: %s", type(err).__name__, err)
    return None


def _extract_header_format_from_lines(lines: List[str]) -> str:
    """Extract header from list of lines.

    Args:
        lines (list): List of str, each element is a line of the loaded chat.

    Returns:
        str: Format of the header.

    """
    # Obtain header format from list of lines
    elements_list, template_list = _extract_elements_template_from_lines(lines)
    return _extract_header_format_from_components(elements_list, template_list)


def _extract_elements_template_from_lines(lines: List[str]) -> Tuple[List[List[int]], List[str]]:
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


def _extract_possible_header_from_line(line: str) -> Optional[str]:
    """Given a `line` extract possible header. Uses ':' as separator.

    Args:
        line (str): Line containing header and message body.

    Returns:
        str: Possible header.

    """
    # Extract possible header from line
    line_split = line.split(": ")
    if len(line_split) >= 2:
        # possible header
        header = line_split[0]
        if not header.isprintable():
            # Not necessarily an error: e.g. usernames with compound emojis contain a Zero Width Joiner (U+200D).
            logging.debug("Header contains unprintable characters: %r", header)
        if header[-1] != ":":
            header += ":"
        return header
    return None


def _extract_header_parts(header: str) -> Tuple[List[int], str]:
    """Extract all parts from header (i.e. date elements and name).

    Args:
        header (str): Header.

    Returns:
        tuple: Contains two elements, (i) list with components and (ii) string template which specifies the formatting
                of the components.

    """

    def _get_last_idx_digit(v: str, i: int) -> int:
        if i + 1 < len(v):
            if v[i + 1].isdigit():
                return _get_last_idx_digit(v, i + 1)
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
    hformat_template = ""
    i = 0
    while i < len(header):
        if header[i].isdigit():
            j = _get_last_idx_digit(header, i)
            hformat_elements.append(int(header[i : j + 1]))
            hformat_template += "{}"
            i = j
        else:
            hformat_template += header[i]
        i += 1
    items = re.findall(r"[-|\]]\s[^:]*:", hformat_template)
    if len(items) != 1:
        raise RegexError(
            "Username match was not possible. Check that header (%s) is of format '... - %name:' or '[...] %name:'",
            hformat_template,
        )
    hformat_template = hformat_template.replace(items[0][2:-1], "%name")
    code = " %p"
    hformat_template = (
        hformat_template.replace(" PM", code)
        .replace(" AM", code)
        .replace(" A.M.", code)
        .replace(" P.M.", code)
        .replace(" am", code)
        .replace(" pm", code)
        .replace(" a.m.", code)
        .replace(" p.m.", code)
    )
    return hformat_elements, hformat_template


def _score_date_order(dates_df: pd.DataFrame, day_pos: int, month_pos: int, year_pos: int) -> Optional[int]:
    """Score how well one day/month/year assignment fits the numbers actually seen in the chat.

    Returns None when the assignment is impossible — a month above 12, a day above 31, or a year
    that is neither consistently 2-digit nor consistently 4-digit. Otherwise a higher score means
    more corroborating evidence.

    Args:
        dates_df (pandas.DataFrame): Numeric header components, one row per header.
        day_pos (int): Candidate column for the day.
        month_pos (int): Candidate column for the month.
        year_pos (int): Candidate column for the year.

    Returns:
        int, optional: Score, or None if the assignment contradicts the data.
    """
    day, month, year = dates_df[day_pos], dates_df[month_pos], dates_df[year_pos]

    if not month.between(1, 12).all() or not day.between(1, 31).all():
        return None
    four_digit = bool(year.between(1000, 9999).all())
    if not (four_digit or year.between(0, 99).all()):
        return None

    score = 0
    if four_digit:
        score += 6  # a 4-digit value can only be the year
        if bool((day > 12).any()):
            score += 2  # with the year already identified, a value above 12 cannot be a month

    # How much each field varies is the discriminator when every value could pass for any field,
    # which is the usual situation with a 2-digit year. Across one chat the day moves, the month
    # moves less and the year barely at all.
    # int(): these are Series, so nunique() is a count, but the stubs widen it.
    n_day, n_month, n_year = int(day.nunique()), int(month.nunique()), int(year.nunique())
    if n_day >= n_month:
        score += 3
    if n_year <= n_month:
        score += 3

    if bool((day > 27).any()):
        score += 2  # 28-31 is a day; as a 2-digit year it would be in the future
    # An export is written in chronological order, so the right reading runs forwards.
    chronological = list(zip(year, month, day, strict=True))
    if chronological == sorted(chronological):
        score += 3
    return score


def _infer_date_positions(dates_df: pd.DataFrame) -> Tuple[int, int, int]:
    """Work out which of the first three numeric columns hold the day, month and year.

    Every ordering is scored against the observed values rather than picking the day by looking for
    a value between 28 and 31. That lookup silently fell back to the first column on any chat that
    never reaches day 28, which mis-detected 72 of the 96 supported formats and could swap day and
    year without raising anything.

    Args:
        dates_df (pandas.DataFrame): Numeric header components, one row per header.

    Returns:
        tuple: (day_pos, month_pos, year_pos).
    """
    best, best_score = None, None
    for day_pos, month_pos, year_pos in itertools.permutations((0, 1, 2)):
        score = _score_date_order(dates_df, day_pos, month_pos, year_pos)
        if score is None:
            continue
        # Ties keep the first ordering tried, which makes the result deterministic.
        if best_score is None or score > best_score:
            best, best_score = (day_pos, month_pos, year_pos), score

    if best is None:
        # Nothing fits; fall back to the original guess rather than refusing to parse at all.
        # Restricted to the date columns: the original lookup searched every column and could
        # return the minutes, whose values sit in the same 28-31 range.
        date_max = dates_df[[0, 1, 2]].max()
        day_pos = cast(int, ((date_max > 27) & (date_max < 32)).idxmax())
        remaining = [p for p in (0, 1, 2) if p != day_pos]
        year_pos = cast(int, dates_df[remaining].max().idxmax())
        month_pos = next(p for p in remaining if p != year_pos)
        return day_pos, month_pos, year_pos
    return best


def _extract_header_format_from_components(elements_list: List[List[int]], template_list: List[str]) -> str:
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
    for e, t in zip(elements_list, template_list, strict=True):
        if (len(e) == len_mode) and ("".join([str(type(ee).__name__) for ee in e]) == type_mode):
            elements_list_.append(e)
            template_list_.append(t)
    # Get positions
    df = pd.DataFrame(elements_list_)
    # dates_df = df.select_dtypes(int)
    dates_df = df.select_dtypes("number")
    # template_list_ is the outlier-filtered list built just above; reading template_list here
    # defeated that filtering and let a single odd first line pick the format for the whole chat.
    template = template_list_[0]

    if "%p" in template:
        hour_code = "%I"
    else:
        hour_code = "%H"

    day_pos, month_pos, year_pos = _infer_date_positions(dates_df)
    dates_df = dates_df.drop(columns=[day_pos, year_pos, month_pos])
    # Hour
    hour_pos = 3
    dates_df = dates_df.drop(columns=[hour_pos])
    # Minute
    minutes_pos = 4
    dates_df = dates_df.drop(columns=[minutes_pos])
    # Dictionary with positions and date element code
    dates_pos = {day_pos: "%d", year_pos: "%y", month_pos: "%m", hour_pos: hour_code, minutes_pos: "%M"}
    # Seconds
    if dates_df.shape[1] > 0:
        seconds_pos = 5
        dates_pos[seconds_pos] = "%S"

    keys_ordered = sorted(dates_pos.keys())
    dates_codes = [dates_pos[k] for k in keys_ordered]

    codes = dates_codes + ["%name"]
    # print(codes)
    # print(template)
    # print(template)
    # print(codes)
    code_template = template.format(*codes)
    # print(code_template)
    # print('---------------')
    # print(code_template)
    return code_template
