""""
Do what you want with this script - ColonolNutty
"""
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.enums.interactions_enum import CommonInteractionId
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from os.path import dirname
from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """ Mod info. """
    _FILE_PATH: str = str(dirname(dirname(dirname(__file__))))

    @property
    def _name(self) -> str:
        return 'NoSitWhileChatting'

    @property
    def _author(self) -> str:
        return 'ColonolNutty'

    @property
    def _base_namespace(self) -> str:
        return 'no_sit_while_chat'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '1.0'


class NoSitWhileChattingMod:
    """A class used for storing variables."""
    NO_SIT_ALLOWED = True

    @classmethod
    def is_chatting(cls, sim_info: SimInfo) -> bool:
        """Whether or not the Sim is chatting."""
        # sim_Toddler_Talk
        toddler_talk = 140885
        return CommonSimInteractionUtils.has_interactions_running_or_queued(sim_info, (CommonInteractionId.SIM_CHAT, toddler_talk))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Sim, Sim.in_non_adjustable_posture.__name__)
def _no_sit_override_social_adjustment(original, self, *_, **__) -> bool:
    sim_info = CommonSimUtils.get_sim_info(self)
    if not CommonSimInteractionUtils.is_standing(sim_info):
        return original(self, *_, **__)
    if NoSitWhileChattingMod.is_chatting(sim_info):
        return False
    return original(self, *_, **__)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _no_sit_prevent_sit_while_chatting(event_data: S4CLInteractionQueuedEvent):
    if not CommonZoneSpinEventDispatcher().game_loaded:
        return True
    if NoSitWhileChattingMod.NO_SIT_ALLOWED:
        if NoSitWhileChattingMod.is_chatting(event_data.queuing_sim_info):
            lowered_interaction = str(event_data.interaction).lower()
            if 'social_adjustment' in lowered_interaction:
                return False
    return True


@CommonConsoleCommand(ModInfo.get_identity(), 'no_sit.toggle', 'Toggle the No Sit While Chatting mod on or off.')
def _no_sit_toggle(output: CommonConsoleCommandOutput):
    NoSitWhileChattingMod.NO_SIT_ALLOWED = not NoSitWhileChattingMod.NO_SIT_ALLOWED
    if NoSitWhileChattingMod.NO_SIT_ALLOWED:
        output('NoSitWhileChatting has been enabled!')
    else:
        output('NoSitWhileChatting has been disabled!')


@CommonConsoleCommand(ModInfo.get_identity(), 'no_sit.status', 'Check the status of the No Sit While Chatting mod.')
def _no_sit_check(output: CommonConsoleCommandOutput):
    if NoSitWhileChattingMod.NO_SIT_ALLOWED:
        output('NoSitWhileChatting is currently enabled.')
    else:
        output('NoSitWhileChatting is currently disabled.')
