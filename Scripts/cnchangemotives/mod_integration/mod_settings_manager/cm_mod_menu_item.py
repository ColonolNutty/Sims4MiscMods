"""
This file is part of Change Motives licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    from typing import Callable, Any, Union
    from protocolbuffers.Localization_pb2 import LocalizedString
    from sims.sim_info import SimInfo
    from event_testing.results import TestResult
    from sims4modsettingsmenu.registration.mod_settings_menu_item import S4MSMMenuItem
    from sims4modsettingsmenu.registration.mod_settings_registry import S4MSMModSettingsRegistry
    from sims4communitylib.mod_support.mod_identity import CommonModIdentity
    from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
    from sims4communitylib.utils.common_type_utils import CommonTypeUtils
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry
    from sims4.resources import Types
    from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
    from cnchangemotives.dialogs.change_motives_dialog import CMChangeMotivesDialog
    from cnchangemotives.enums.string_ids import CMStringId
    from cnchangemotives.interactions.change_motives import CMChangeMotivesInteraction
    from cnchangemotives.modinfo import ModInfo


    class _CMMSMMenuItem(S4MSMMenuItem):
        # noinspection PyMissingOrEmptyDocstring
        @property
        def title(self) -> Union[int, str, LocalizedString]:
            return CMStringId.CHANGE_MOTIVES

        # noinspection PyMissingOrEmptyDocstring
        @property
        def description(self) -> Union[int, str, LocalizedString]:
            return CMStringId.CHANGE_MOTIVE_LEVELS_OF_A_SIM

        # noinspection PyMissingOrEmptyDocstring
        @property
        def mod_identity(self) -> CommonModIdentity:
            return ModInfo.get_identity()

        # noinspection PyMissingOrEmptyDocstring
        @property
        def log_identifier(self) -> str:
            return 'cm_msm_menu_item'

        # noinspection PyMissingOrEmptyDocstring
        def is_available_for(self, source_sim_info: SimInfo, target: Any=None) -> bool:
            self.log.debug('Checking if Change Motives dialog is available for \'{}\' and Target \'{}\'.'.format(CommonSimNameUtils.get_full_name(source_sim_info), target))
            if target is None or not CommonTypeUtils.is_sim_or_sim_info(target):
                self.log.debug('Target is not a Sim.')
                return False
            self.log.debug('Change Motives menu is available for Source Sim and Target Sim.')
            return True

        # noinspection PyMissingOrEmptyDocstring
        def show(
            self,
            source_sim_info: SimInfo,
            *args,
            target: Any=None,
            on_close: Callable[..., Any]=CommonFunctionUtils.noop,
            **kwargs
        ):
            self.log.debug('Showing Change Motives dialog.')
            if target is None:
                if on_close is not None:
                    on_close()
                return
            target_sim_info = CommonSimUtils.get_sim_info(target)
            CMChangeMotivesDialog(on_close=on_close).open(target_sim_info)


    S4MSMModSettingsRegistry().register_menu_item(_CMMSMMenuItem())

    log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'cm_change_motives')

    # noinspection PyUnusedLocal
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CMChangeMotivesInteraction, CMChangeMotivesInteraction.on_test.__name__)
    def _cm_hide_interaction(original, cls, *_, **__) -> TestResult:
        log.debug('Hiding the CM Change Motives interaction in favor of the Mod Settings Menu.')
        return TestResult.NONE
except:
    pass
