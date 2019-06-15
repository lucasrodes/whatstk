from collections import defaultdict
import pandas as pd


# %%
# TODO: document
def user_interventions(chat, timestep = 'days', length = False):
    if timestep == 'days':
        return user_interventions_days(chat.parsed_chat, length)
    # elif timestep == 'hours':
    #    return user_interventions_hours(chat.parsed_chat)
    else:
        return 0


# %%
def user_interventions_days(data, length=False):
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)

    Parameters
    ----------
    data: list
        DataFrame containing the interventions of all users, including the text.

    Returns
    ----------
    df: DataFrame
        Table containing #interventions per user per each day
        :param data:
        :param length:
        :return:
    """

    dix = defaultdict(dict)

    for d in data:
        date = d[0].date()
        user = d[1]
        if length:
            dix[date][user] = dix[date].get(user, 0) + len(d[2])
        else:
            dix[date][user] = dix[date].get(user, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    return df


# %%
def user_interventions_hours(data):
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)

    Parameters
    ----------
    data: DataFrame
        DataFrame containing the interventions of all users, including the text.

    Returns
    ----------
    df: DataFrame
        Table containing #interventions per user per each day
    """

    dix = defaultdict(dict)

    for d in data:
        date_with_hour = str(d[0].date()) + ' ' + str(d[0].hour)
        user = d[1]
        dix[date_with_hour][user] = dix[date_with_hour].get(user, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    return df


# %%
def week_hour_grid(chat):
    """
    Return DataFrame with interventions of all users (columns) for all days (rows)
        :param chat: DataFrame containing the interventions of all users, including the text.
        :return: DataFrame containing #interventions per user per each day and hour
    """
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    dix = defaultdict(dict)
    count = 0
    for d in chat.parsed_chat:
        hour = (d[0].hour - 8)
        if hour < 0:
            count += 1
            day = weekdays[(d[0].weekday() - 1) % 7]
        else:
            day = weekdays[d[0].weekday()]
        hour = hour % 24
        dix[day][hour] = dix[day].get(hour, 0) + 1

    df = pd.DataFrame.from_dict(dix, orient='index')
    df = df.fillna(0)
    df = df.reindex(
        index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
               'Saturday', 'Sunday'],
        columns=list(range(0, 24)))
    print(count)
    return df


# %%
def response_matrix(chat, ptype='absolute'):
    """
    Obtains the response matrix between users in the chat group
        :param chat: DataFrame containing the interventions of all users, including the text.
        :param ptype: Options for the response matrix (normalized, conditional probabilities etc.)
        :return: Response matrix as DataFrame
    """
    dix = defaultdict(dict)
    for user in chat.usernames:
        dix[user][user] = 0
    for i in range(1, len(chat.parsed_chat)):
        user_old = chat.parsed_chat[i - 1][1]
        user_new = chat.parsed_chat[i][1]
        if user_old != user_new:
            dix[user_old][user_new] = dix[user_old].get(user_new, 0) + 1

    df = pd.DataFrame.from_dict(dix)

    if ptype != 'absolute':
        df /= df.sum().sum()
        if ptype == 'joint':
            df = df
        elif ptype == 'conditional_replier':
            df = df.divide(df.sum(axis=1), axis=0)
        elif ptype == 'conditional_replied':
            df /= df.sum(axis=0)
        df = df.fillna(0)
        df *= 100

    df = df.fillna(0)
    return df


# %%
def histogram_intervention_length(chat):
    """
        Obtains the response matrix between users in the chat group
            :param chat: DataFrame containing the interventions of all users, including the text.
            :return:
        """
    dix = defaultdict(list)

    for intervention in chat.parsed_chat:
        if intervention[2] != "<Media omitted>" and len(intervention[2]) != 0:
            dix["user"].append(intervention[1])
            dix["length"].append(len(intervention[2]))
            dix["intervention"].append(intervention[2])

    return pd.DataFrame(dix)


# TODO: RETHING LOOP AS IN THE ONE ABOVE
'''def get_intervention_table_hoursday(users, hours, data):
    """
"""Return DataFrame with interventions of all users (columns) for all hour times (rows)

    Parameters
    ----------
    users: list
        List with the usernames of the chat.
    hours: list
        Hours the chat has been active.
    data: list
        Legible data.

    Returns
    ----------
    df: Dataframe
        Table containing #interventions per user per each hour of the day
    """
"""
    interventions_per_hour = np.zeros(len(hours))

    # Loop for all users
    df = pd.DataFrame()
    for user in users:
        interventions = get_interventions_user(user, data)
        # Obtain number of interventions per each day contained in hours
        for i in range(len(hours)):
            interventions_per_hour[i] = get_number_interventions_per_hour(hours[i],
                                                                          interventions)
        inter = pd.Series(interventions_per_hour, index=hours)
        df.insert(0, user, inter)

    return df


def get_list_interventions_user(username, data):
    """
    Obtains a list with all interventions of username_

    Parameters
    ----------
    username_: list
        Days the chat has been active.
    data_: list
        Legible data.

    Returns
    ----------
    list
        List of dates (nicely written) the chat has been active
    """
    return [d for d in data if d[1] == username]


def get_number_interventions_per_day(day_, interv_):
    """
    Obtains the number of interventions in the day 'day_'

    Parameters
    ----------
    day_: list
        Day we are examining.
    interv_: list
        List containing all considered interventions.

    Returns
    ----------
    list
        List containing two parameters. The first one quantifies the number
        of interventions in day 'day_'. The second one is just the index of
        the last intervention in 'day_' to make the overall search more
        efficient
    """

    s = [1 if i[0][:3] == day_ else 0 for i in interv_]
    if s[-1] == 0:
        i = s.index(0)
    else:
        i = -1
    return [sum(s), i]



def get_number_interventions_per_hour(hour_, interv_):
    """
    Obtains the number of interventions during the hour 'hour_'

    Parameters
    ----------
    hour_: list
        Hour we are examining.
    interv_: list
        List containing all considered interventions.

    Returns
    ----------
    int
        quantifies the number of interventions during 'hour_'.
    """
    s = [1 if i[0][3] == hour_ else 0 for i in interv_]
    return sum(s)
'''

"""
REFERENCES
----------

[1] MiniQuark comment,
http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string

[2] Comment from Mark Byers,
http://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists

[3] Function from Jer42
http://stackoverflow.com/a/31607735
"""