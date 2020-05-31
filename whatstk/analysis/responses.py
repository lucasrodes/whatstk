"""Get infor regarding responses between users."""


from collections import namedtuple
import pandas as pd
from whatstk.objects import WhatsAppChat
from whatstk.utils.utils import _get_df, COLNAMES_DF


Norms = namedtuple('Norms', ['ABSOLUTE', 'JOINT', 'SENDER', 'RECEIVER'])
NORMS = Norms(
    ABSOLUTE='absolute',
    JOINT='joint',
    SENDER='sender',
    RECEIVER='receiver'
)


def response_matrix(df=None, chat=None, zero_own=True, norm=NORMS.ABSOLUTE):
    """Get response matrix for given chat.

    Obtains a DataFrame of shape [n_users, n_users] counting the number of responses between members. Responses can be
    counted in different ways, e.g. using absolute values or normalised values. Responses are counted based solely on
    consecutive messages. That is, if user_i sends a message right after user_j, it will be counted as a response from
    user_i to user_j.

    Axis 0 lists senders and axis 1 lists receivers. That is, the value in cell (i, j) denotes the number of times
    user_i responded to a message from user_j.

    Args:
        df (pandas.DataFrame, optional): Chat. Defaults to None.
        chat (WhatsAppChat, optional): Chat. Defaults to None.
        zero_own (bool, optional): Set to True to avoid counting own responses. Defaults to True.
        norm (str, optional): Specifies the type of normalization used for reponse count.

    Returns:
        pandas.DataFrame: Response matrix.

    Example:

        Get absolute count on responses (consecutive messages) between users

        ```python
        >>> from whatstk import df_from_txt
        >>> from whatstk.analysis.responses import response_matrix
        >>> df = df_from_txt(path)
        >>> responses = response_matrix(df)
        ```

        Get percentage of responses received for each user.

        ```python
        >>> from whatstk import df_from_txt
        >>> from whatstk.analysis.responses import response_matrix
        >>> df = df_from_txt(path)
        >>> responses = response_matrix(df, norm='receive)
        ```

    """
    # Get chat df and users
    df = _get_df(df=df, chat=chat)
    users = WhatsAppChat(df).users
    # Get list of username transitions and initialize dicitonary with counts
    user_transitions = df[COLNAMES_DF.USERNAME].tolist()
    responses = {user: dict(zip(users, [0]*len(users))) for user in users}
    # Fill count dictionary
    for i in range(1, len(user_transitions)):
        sender = user_transitions[i]
        receiver = user_transitions[i-1]
        if zero_own and (sender != receiver):
            responses[sender][receiver] += 1
        elif not zero_own:
            responses[sender][receiver] += 1
    responses = pd.DataFrame.from_dict(responses, orient='index')

    # Normalize
    if norm not in [NORMS.ABSOLUTE, NORMS.JOINT, NORMS.RECEIVER, NORMS.SENDER]:
        raise ValueError("norm not valid. See NORMS variable in whatstk.analysis.resposes")
    else:
        if norm == NORMS.JOINT:
            responses /= responses.sum().sum()
        elif norm == NORMS.RECEIVER:
            responses /= responses.sum(axis=0)
        elif norm == NORMS.SENDER:
            responses = responses.divide(responses.sum(axis=1), axis=0)
    return responses
