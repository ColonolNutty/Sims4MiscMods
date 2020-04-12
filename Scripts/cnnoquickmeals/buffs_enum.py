# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class NQMBuffId(Int):
    """ Buff Identifiers used by NQM. """
    QUICK_MEALS_INAPPROPRIATE = 501519620710818897
