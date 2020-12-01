from typing import Tuple

from cnnoquickmeals.modinfo import ModInfo
from interactions.base.interaction import Interaction
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils


class NQMInteractionBlocker(CommonService, HasLog):
    """ Blocks quick meal interactions. """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'no_quick_meal'

    def get_quick_meal_interactions(self) -> Tuple[int]:
        result: Tuple[int] = (
            # fridge_GrabCookiesAutonomously
            181585,
            # fridge_GrabSnackAutonomously
            13397,
            # fridge_GrabSnack_Autotest
            111967,
            # fridge_GrabSnack_Microwave_PieMenu
            217063,
            # fridge_GrabSnack_PieMenu
            77672,
            # fridge_GrabWaterAutonomously
            164355,
        )
        return result

    def should_allow_interaction(self, interaction: Interaction) -> bool:
        """ Block interactions in the queue. """
        interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
        if interaction_id in self.get_quick_meal_interactions():
            self.log.debug('Interaction is quick meal!')
            return False
        interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction)
        if interaction_name is None:
            return True
        if self._is_quick_meal(interaction_name):
            return False
        return True

    def _is_quick_meal(self, interaction_name: str) -> bool:
        # noinspection SpellCheckingInspection
        quick_meal_names: Tuple[str] = (
            'fridge_GrabCookiesAutonomously',
            'fridge_GrabSackLunch',
            'fridge_GrabSnackAutonomously',
            'fridge_GrabSnack_Autotest',
            'fridge_GrabSnack_Microwave_PieMenu',
            'fridge_GrabSnack_PieMenu',
            'fridge_GrabWaterAutonomously',
            'SrslySims:StartCrafting_Fridge_SnacksDESSERT-Custom',
            'SrslySims:StartCrafting_Fridge_SnacksDRINKS-Custom',
            'SrslySims:StartCrafting_Fridge_SnacksHEALTHY-Custom',
            'SrslySims:StartCrafting_Fridge_SnacksJUNKFOOD-Custom',
            'SrslySims:StartCrafting_Fridge_SnacksQUICKMEAL-Custom',
            'SrslySims:StartCrafting_Fridge_ToddlerDRINKS-Custom',
            'SrslySims:StartCrafting_Fridge_ToddlerFOOD-Custom',
        )
        lower_name = interaction_name.lower()
        for name in quick_meal_names:
            if lower_name.startswith(name):
                return True
        return False

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _nqm_block_quick_meal_interactions(event_data: S4CLInteractionQueuedEvent) -> bool:
        if not CommonZoneSpinEventDispatcher().game_loaded:
            return True
        return NQMInteractionBlocker().should_allow_interaction(event_data.interaction)
