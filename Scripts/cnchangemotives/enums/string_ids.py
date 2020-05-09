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
    CHANGE_MOTIVE_LEVELS_OF_A_SIM = 4062147760
    CHOOSE_MOTIVE_TO_SET = 1553522236
    SET_ALL_MOTIVE_LEVELS_TO_MINIMUM = 183466032
    # Tokens: {0.SimFirstName}
    SET_ALL_MOTIVE_LEVELS_TO_MINIMUM_CONFIRMATION = 4249870684
    SET_ALL_MOTIVE_LEVELS_TO_MAXIMUM = 3926553886
    # Tokens: {0.String} {1.SimFirstName} {1.SimLastName}
    SET_MOTIVE_LEVEL_OF_SIM = 2845688704
    # Tokens: {0.String}
    MIN_AND_MAX = 2860408691

    # Motive Names
    ENERGY = 2289465258
    BLADDER = 3516699461
    BOWEL = 1152798790
    FUN = 39540353
    HUNGER = 1918738815
    HYGIENE = 356487851
    SOCIAL = 3697845997
    VAMPIRE_ENERGY = 33440810
    THIRST = 2210315635
    WATER = 917413649
    HYDRATION = 1732449457
    DURABILITY = 4267725152
    CHARGE = 4285247397
