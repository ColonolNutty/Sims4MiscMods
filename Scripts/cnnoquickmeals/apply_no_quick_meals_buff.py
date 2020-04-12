from cnnoquickmeals.buffs_enum import NQMBuffId
from cnnoquickmeals.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils


class NQMBuffUtils(CommonService, HasLog):
    """ Buff Utils for NQM. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'nqm_buff_utils'

    def apply_no_quick_meals_buff(self) -> bool:
        """ Apply a buff that disables Quick Meals. """
        self.log.debug('Attempting to apply NQM buff.')

        def _is_valid_sim(_sim_info: SimInfo) -> bool:
            return CommonSpeciesUtils.is_human(_sim_info) and not CommonAgeUtils.is_baby(_sim_info)

        for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=_is_valid_sim):
            sim_name = CommonSimNameUtils.get_full_name(sim_info)
            if CommonBuffUtils.has_buff(sim_info, NQMBuffId.QUICK_MEALS_INAPPROPRIATE):
                self.log.debug('Ignoring, \'{}\' already has NQM buff.'.format(sim_name))
                continue
            self.log.debug('Adding NQM buff to \'{}\'.'.format(sim_name))
            CommonBuffUtils.add_buff(sim_info, NQMBuffId.QUICK_MEALS_INAPPROPRIATE)
        self.log.debug('Done adding NQM buff.')
        return True

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _apply_buffs_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        NQMBuffUtils().log.enable()
        return NQMBuffUtils().apply_no_quick_meals_buff()
