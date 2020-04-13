"""
Offer Blood is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY ND 4.0).

http://creativecommons.org/licenses/by-nd/4.0/
http://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class OBInteractionId(Int):
    """ Interaction Ids used by OB. """
    OFFER_TO_DRINK = 7787402245494911477
