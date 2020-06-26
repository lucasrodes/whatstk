"""Get infor regarding responses between users."""


from collections import namedtuple
import pandas as pd
from whatstk.whatsapp.objects import WhatsAppChat
from whatstk.utils.utils import _get_df, COLNAMES_DF


Norms = namedtuple('Norms', ['ABSOLUTE', 'JOINT', 'SENDER', 'RECEIVER'])
NORMS = Norms(
    ABSOLUTE='absolute',
    JOINT='joint',
    SENDER='sender',
    RECEIVER='receiver'
)


def get_response_matrix(df=None, chat=None, zero_own=True, norm=NORMS.ABSOLUTE):
    """Get response matrix for given chat.

    Obtains a DataFrame of shape `[n_users, n_users]` counting the number of responses between members. Responses can
    be counted in different ways, e.g. using absolute values or normalised values. Responses are counted based solely
    on consecutive messages. That is, if :math:`user_i` sends a message right after :math:`user_j`, it will be counted
    as a response from :math:`user_i` to :math:`user_j`.

    Axis 0 lists senders and axis 1 lists receivers. That is, the value in cell (i, j) denotes the number of times
    :math:`user_i` responded to a message from :math:`user_j`.

    **Note**: Either ``df`` or ``chat`` must be provided.

    Args:
        df (pandas.DataFrame, optional): Chat data. Atribute `df` of a chat loaded using Chat. If a value is given,
                                            ``chat`` is ignored.
        chat (Chat, optional): Chat data. Object obtained when chat loaded using Chat. Required if ``df`` is None.
        zero_own (bool, optional): Set to True to avoid counting own responses. Defaults to True.
        norm (str, optional): Specifies the type of normalization used for reponse count. Can be:

                                - ``'absolute'``: Absolute count of messages.
                                - ``'joint'``: Normalized by total number of messages sent by all users.
                                - ``'sender'``: Normalized per sender by total number of messages sent by user.
                                - ``'receiver'``: Normalized per receiver by total number of messages sent by user.

    Returns:
        pandas.DataFrame: Response matrix.

    Example:
            Get absolute count on responses (consecutive messages) between users.

            ..  code-block:: python

                >>> from whatstk import WhatsAppChat
                >>> from whatstk.analysis import get_response_matrix
                >>> from whatstk.data import whatsapp_urls
                >>> chat = WhatsAppChat.from_source(filepath=whatsapp_urls.POKEMON)
                >>> responses = get_response_matrix(chat=chat)
                >>> responses
                                Ash Ketchum  Brock  ...  Raichu  Wobbuffet
                Ash Ketchum               0      0  ...       1          0
                Brock                     1      0  ...       0          0
                Jessie & James            0      1  ...       0          0
                Meowth                    0      0  ...       0          0
                Misty                     2      1  ...       1          0
                Prof. Oak                 0      1  ...       0          0
                Raichu                    1      0  ...       0          0
                Wobbuffet                 0      0  ...       0          0

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
