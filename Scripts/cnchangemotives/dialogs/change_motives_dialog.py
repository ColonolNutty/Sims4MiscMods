"""
This file is part of Change Motives licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Tuple

from cnchangemotives.enums.string_ids import CMStringId
from cnchangemotives.modinfo import ModInfo
from cnchangemotives.utils.motive_utils import CMMotiveUtils
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CMChangeMotivesDialog(CommonService, HasLog):
    """ A dialog for changing Sim motives. """
    def __init__(self) -> None:
        super().__init__()
        self.motive_utils = CMMotiveUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'cm_change_motives_dialog'

    def open(self, sim_info: SimInfo, on_close: Callable[..., Any]=None) -> None:
        """ Open the dialog. """
        self.log.debug('Opening change motives dialog for \'{}\'.'.format(CommonSimNameUtils.get_full_name(sim_info)))

        def _on_close() -> None:
            if on_close is not None:
                on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CMStringId.CHANGE_MOTIVES,
            CMStringId.CHOOSE_MOTIVE_TO_SET,
            mod_identity=self.mod_identity,
            on_close=_on_close
        )

        def _reopen_dialog() -> None:
            self.open(sim_info, on_close=on_close)

        def _on_min_all_motives() -> None:
            def _on_confirm(_) -> None:
                self.motive_utils.min_all_motives(sim_info)
                _reopen_dialog()

            def _on_cancel(_) -> None:
                _reopen_dialog()

            CommonOkCancelDialog(
                CMStringId.CONFIRMATION,
                CMStringId.SET_ALL_MOTIVE_LEVELS_TO_MINIMUM_CONFIRMATION,
                description_tokens=(sim_info,),
                mod_identity=self.mod_identity
            ).show(on_ok_selected=_on_confirm, on_cancel_selected=_on_cancel)

        def _on_max_all_motives() -> None:
            self.motive_utils.max_all_motives(sim_info)

        def _on_slider_changed(chosen_motive_name: str, amount: float, outcome: CommonChoiceOutcome):
            if chosen_motive_name is None or amount is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen_dialog()
                return
            self.motive_utils.change_motive_level(sim_info, chosen_motive_name, amount)
            _reopen_dialog()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CMStringId.SET_ALL_MOTIVE_LEVELS_TO_MINIMUM,
                    0,
                ),
                on_chosen=lambda *_, **__: _on_min_all_motives(),
                always_visible=True
            ),
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    CMStringId.SET_ALL_MOTIVE_LEVELS_TO_MAXIMUM,
                    0,
                ),
                on_chosen=lambda *_, **__: _on_max_all_motives(),
                always_visible=True
            ),
        )

        motive_names: Tuple[str] = CMMotiveUtils().get_valid_motives(sim_info)
        sorted_motive_names = sorted(motive_names, key=lambda s: s)
        for motive_name in sorted_motive_names:
            if motive_name is None:
                return

            motive_string_id = CMMotiveUtils().get_motive_string(sim_info, motive_name)
            if motive_string_id == -1:
                motive_string_id = motive_name.upper()

            option_dialog.add_option(
                CommonDialogInputFloatOption(
                    motive_name,
                    self.motive_utils.get_motive_level(sim_info, motive_name),
                    CommonDialogOptionContext(
                        motive_string_id,
                        CMStringId.SET_MOTIVE_LEVEL_OF_SIM,
                        description_tokens=(motive_string_id, sim_info)
                    ),
                    min_value=-100.0,
                    max_value=100.0,
                    on_chosen=_on_slider_changed,
                    dialog_description_identifier=CMStringId.MIN_AND_MAX,
                    dialog_description_tokens=(CommonLocalizationUtils.create_localized_string(CMStringId.SET_MOTIVE_LEVEL_OF_SIM, tokens=(motive_string_id, sim_info)),)
                )
            )

        option_dialog.show(sim_info=sim_info)
