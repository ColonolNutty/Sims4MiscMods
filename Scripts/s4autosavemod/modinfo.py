"""
This file is part of the S4 Autosave Mod licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """ Mod info for the Mod. """
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'AutosaveMod'

    @property
    def _author(self) -> str:
        return 'ColonolNutty'

    @property
    def _base_namespace(self) -> str:
        return 's4autosavemod'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH
