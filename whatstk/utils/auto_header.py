import pandas as pd
import logging


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
    except:
        logging.info("Format not found.")
    return None
    
def issep(s):
    """Check if `s` is a separator character.

    Separator can be one of the following: '.', ',', '-', '/', ':', '[' or ']'.

    Args:
        s (str): Character to be checked.

    Returns:
        bool: True if `s` is a separator, False otherwise.

    """
    if s in separators:
        return True
    return False


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
    fheaders = []
    elements_list = []
    template_list = []
    for line in lines:
        header = _extract_possible_header_from_line(line)
        if header:
            elements, template = _extract_header_parts(header)
            elements_list.append(elements)
            template_list.append(template)
    return elements_list, template_list


def _extract_possible_header_from_line(line):
    """Given a `line` extract possible header.

    Args:
        line (str): Line containing header and message body.

    Returns:
        str: Possible header.

    """
    # Extract possible header from line
    line_split = line.split(': ')
    if len(line_split)>=2:
        # possible header
        header = line_split[0]
        if not header.isprintable():
            header = header.replace('\u200e', '').replace('\u202e', '')
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
    # Given header, obtain template (for format) and elements
    b = []
    t = ""
    is_num = False
    e_cum = ""
    push = False
    l = len(header)
    count = 0

    # Replace PM/AM/a.m./p.m. to "%P"
    code = " %p"
    header = header.replace(' PM', code)\
                    .replace(' AM', code)\
                    .replace(' a.m.', code)\
                    .replace(' p.m.', code)
    count = 0
    for i in range(len(header)):
        if count >= len(header):
            break
        e = header[count]
        # Push element to b
        if header[count: count+2] == '%p':
            t += "%p"
            count += 1
        elif e.isspace():
            if e_cum and is_num:
                b.append(int(e_cum))
                e_cum = ""
                is_num = False
                t += '{} '
            elif e_cum and not is_num:
                e_cum += " "
            elif t:
                if issep(t[-1]):
                    t += ' '
        elif issep(e):
            if e_cum:
                b.append(int(e_cum) if is_num else e_cum)
                e_cum = ""
                is_num = False
                t += '{}'
            if e == '[':
                t += '\['
            elif e == ']':
                t += '\]'
            else:
                t += e
        elif e.isalpha():
            if e_cum and is_num:
                b.append(int(e_cum))
                e_cum = ""
                is_num = False
                t += '{}'
            e_cum += e
        elif e.isdigit():
            if e_cum and not is_num:
                b.append(e_cum)
                e_cum = ""
                is_num = False
                t += '{}'
            e_cum += e
            is_num = True

        count += 1

    if e_cum.isdigit():
        b.append(int(e_cum))
        t += '{}'
    elif e_cum.replace(' ', '').isalnum():
        b.append(e_cum)
        t += '{}'
    else:
        t += e_cum
    return b, t


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
    l = [len(e) for e in elements_list]
    x = ["".join([str(type(ee).__name__) for ee in e]) for e in elements_list]
    len_mode = max(set(l), key=l.count)
    type_mode = max(set(x), key=x.count)
    for e, t in zip(elements_list, template_list):
        if (len(e)==len_mode) and ("".join([str(type(ee).__name__) for ee in e])==type_mode):
            elements_list_.append(e)
            template_list_.append(t)
    
    # print(elements_list[0])
    # Get positions
    df = pd.DataFrame(elements_list_)
    dates_df = df.select_dtypes(int)

    template = template_list[0]
    
    if '%p' in template:
        hour_code = "%I"
    else:
        hour_code = "%H"

    # day
    day_pos = ((dates_df.max()>27) & (dates_df.max()<32)).idxmax()
    dates_df = dates_df.drop(columns=[day_pos])
    # year
    # year_pos = dates_df.std().idxmin()
    pos = [0,1,2]
    pos.remove(day_pos)
    year_pos = dates_df[pos].max().idxmax()  # Only consider positions 0,1,2
    dates_df = dates_df.drop(columns=[year_pos])
    # Month
    month_pos = dates_df.columns.min()
    dates_df = dates_df.drop(columns=[month_pos])
    # Hour
    hour_pos = 3
    dates_df = dates_df.drop(columns=[hour_pos])
    # Minute
    minutes_pos = 4
    dates_df = dates_df.drop(columns=[minutes_pos])

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
    code_template = template.format(*codes) + ':'
    # print(code_template)
    return code_template
