"""Utils."""


from collections import namedtuple


ColnamesDf = namedtuple('Constants', ['DATE', 'USERNAME', 'MESSAGE', 'MESSAGE_LENGTH'])
COLNAMES_DF = ColnamesDf(
    DATE='date',
    USERNAME='username',
    MESSAGE='message',
    MESSAGE_LENGTH='message_length'
)
