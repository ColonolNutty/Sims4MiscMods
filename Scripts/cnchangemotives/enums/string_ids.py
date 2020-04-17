"""
This file is part of Change Motives licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

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


class CMStringId(Int):
    """ String Ids used by CM. """
    CONFIRMATION = 2520436614
    CHANGE_MOTIVES = 494984776
    CHANGE_MOTIVE = 3137485241
    CHOOSE_MOTIVE_TO_SET = 1553522236
    SET_ALL_MOTIVES_MIN = 2198129887
    # Tokens: {0.SimFirstName}
    SET_ALL_MOTIVES_MIN_CONFIRMATION = 2124109002
    SET_ALL_MOTIVES_MAX = 2063908961
    SET_LEVEL_OF_MOTIVE = 3875423583
