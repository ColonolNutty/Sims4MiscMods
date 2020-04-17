"""
This file is part of Change Motives licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, List

from cnchangemotives.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.enums.enumtypes.string_enum import CommonEnumStringBase
from sims4communitylib.enums.motives_enum import CommonMotiveId
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_motive_utils import CommonSimMotiveUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class CMMotive(CommonEnumStringBase):
    """ Contains names for motives. """
    ENERGY = 'energy'
    BLADDER = 'bladder'
    BOWEL = 'bowel'
    FUN = 'fun'
    HUNGER = 'hunger'
    HYGIENE = 'hygiene'
    SOCIAL = 'social'
    VAMPIRE_POWER = 'vampire_power'
    VAMPIRE_THIRST = 'vampire_thirst'
    PLANT_SIM_WATER = 'plant_sim_water'
    SERVO_DURABILITY = 'servo_durability'
    SERVO_CHARGE = 'servo_charge'


class CMMotiveUtils(CommonService, HasLog):
    """ Utilities for Motives. """
    MOTIVE_MAPPINGS = {
        CMMotive.ENERGY: CommonMotiveId.ENERGY,
        CMMotive.BLADDER: CommonMotiveId.BLADDER,
        CMMotive.FUN: CommonMotiveId.FUN,
        CMMotive.HUNGER: CommonMotiveId.HUNGER,
        CMMotive.HYGIENE: CommonMotiveId.HYGIENE,
        CMMotive.SOCIAL: CommonMotiveId.SOCIAL,
        CMMotive.VAMPIRE_POWER: CommonMotiveId.VAMPIRE_POWER,
        CMMotive.VAMPIRE_THIRST: CommonMotiveId.VAMPIRE_THIRST,
        CMMotive.PLANT_SIM_WATER: CommonMotiveId.PLANT_SIM_WATER,
        CMMotive.SERVO_DURABILITY: CommonMotiveId.SERVO_DURABILITY,
        CMMotive.SERVO_CHARGE: CommonMotiveId.SERVO_CHARGE
    }

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_motive_utils'

    def change_motive_level(self, sim_info: SimInfo, motive_name: str, level: float) -> bool:
        """ Change the level of a motive. """
        if not self.can_translate_motive(sim_info, motive_name):
            return False
        translated_motive_id = self._translate_motive(sim_info, motive_name)
        if translated_motive_id == -1:
            return False
        return CommonSimMotiveUtils.set_motive_level(sim_info, translated_motive_id, level)

    def min_all_motives(self, sim_info: SimInfo) -> bool:
        """ Set all motives for a Sim to the minimum value. """
        for motive_name in CMMotive.values():
            self.change_motive_level(sim_info, motive_name, -100.0)
        return True

    def max_all_motives(self, sim_info: SimInfo) -> bool:
        """ Set all motives for a Sim to the maximum value. """
        for motive_name in CMMotive.values():
            self.change_motive_level(sim_info, motive_name, 100.0)
        return True

    def can_translate_motive(self, sim_info: SimInfo, motive_name: str) -> bool:
        """ Determine if a motive is valid. """
        if motive_name is None:
            return False
        if motive_name == CMMotive.BOWEL:
            if not CommonSpeciesUtils.is_pet(sim_info):
                return False
            return True
        return motive_name in CMMotiveUtils.MOTIVE_MAPPINGS

    def get_motive_level(self, sim_info: SimInfo, motive_name: str) -> float:
        """ Retrieve the current level of a Motive for a Sim. """
        translated_motive_id = self._translate_motive(sim_info, motive_name)
        if translated_motive_id == -1:
            return 0.0
        return CommonSimMotiveUtils._get_motive_level(sim_info, translated_motive_id)

    def get_valid_motives(self, sim_info: SimInfo) -> Tuple[str]:
        """ Retrieve a collection of all valid motives. """
        motives: Tuple[str] = tuple()
        if CommonOccultUtils.is_vampire(sim_info):
            motives += (CMMotive.SOCIAL, CMMotive.FUN, CMMotive.HYGIENE, CMMotive.VAMPIRE_THIRST, CMMotive.VAMPIRE_POWER)
        elif CommonOccultUtils.is_robot(sim_info):
            motives += (CMMotive.SOCIAL, CMMotive.FUN, CMMotive.SERVO_DURABILITY, CMMotive.SERVO_CHARGE)
        elif CommonOccultUtils.is_plant_sim(sim_info):
            motives += (CMMotive.SOCIAL, CMMotive.FUN, CMMotive.HYGIENE, CMMotive.HUNGER, CMMotive.ENERGY, CMMotive.PLANT_SIM_WATER,)
        else:
            motives += (CMMotive.SOCIAL, CMMotive.FUN, CMMotive.HYGIENE, CMMotive.HUNGER, CMMotive.ENERGY, CMMotive.BLADDER)
        if CommonSpeciesUtils.is_pet(sim_info):
            motives += (CMMotive.BOWEL, )
        trimmed_result: List[str] = list()
        for motive in motives:
            trimmed_result.append(motive.replace('CMMotive.', '').lower())
        return tuple(trimmed_result)

    def _translate_motive(self, sim_info: SimInfo, motive_name: str) -> int:
        if motive_name == CMMotive.BOWEL:
            if CommonSpeciesUtils.is_dog(sim_info):
                return CommonMotiveId.PET_DOG_BOWEL
            elif CommonSpeciesUtils.is_cat(sim_info):
                return CommonMotiveId.PET_CAT_BOWEL
            return -1
        else:
            return CMMotiveUtils.MOTIVE_MAPPINGS[motive_name]
