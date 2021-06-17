"""
This file is part of the S4 Autosave Mod licensed under the Creative Commons Attribution-NoDerivatives 4.0 International public license (CC BY-ND 4.0).

https://creativecommons.org/licenses/by-nd/4.0/
https://creativecommons.org/licenses/by-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
import clock
from date_and_time import TimeSpan
from s4autosavemod.modinfo import ModInfo
from services.persistence_service import SaveGameData
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.save_load.common_save_utils import CommonSaveUtils


class _AutosaveHandler:
    _AUTOSAVE_ALARM_HANDLE = None
    _AUTOSAVE_INTERVAL_MINUTES = 15

    @staticmethod
    def _get_autosave_interval() -> TimeSpan:
        return clock.interval_in_real_minutes(_AutosaveHandler._AUTOSAVE_INTERVAL_MINUTES)

    @staticmethod
    def _time_to_save(*_) -> bool:
        try:
            if CommonZoneSpinEventDispatcher().game_loading or not CommonZoneSpinEventDispatcher().game_loaded:
                return False
            CommonBasicNotification(
                'S4ASM Autosaving',
                0
            ).show()
            import sims4.commands
            save_game_data = SaveGameData(CommonSaveUtils.get_save_slot_id(), 'S4ASMAutosave', True, 500001)
            persistence_service = services.get_persistence_service()
            persistence_service.save_using(persistence_service.save_game_gen, save_game_data, send_save_message=True, check_cooldown=False)
            CommonBasicNotification(
                'S4ASM Finished Autosaving',
                0
            ).show()
            return True
        except Exception as ex:
            CommonBasicNotification(
                'Problem Occurred While S4ASM Autosaving',
                0
            ).show()
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'An exception occurred while autosaving.', exception=ex)
            return False

    @staticmethod
    def _register_alarm() -> None:
        has_setup_alarm_before = False
        if _AutosaveHandler._AUTOSAVE_ALARM_HANDLE is not None:
            has_setup_alarm_before = True
            from alarms import _lookup_alarm_handle
            alarm_handle = _lookup_alarm_handle(_AutosaveHandler._AUTOSAVE_ALARM_HANDLE._element_handle)
            if alarm_handle is not None:
                return
            CommonBasicNotification(
                'S4ASM Autosaving Setup Again',
                'S4ASM will autosave every {} minutes real time. Look for the notification!'.format(_AutosaveHandler._AUTOSAVE_INTERVAL_MINUTES)
            ).show()
        from alarms import add_alarm_real_time
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        _AutosaveHandler._AUTOSAVE_ALARM_HANDLE = add_alarm_real_time(CommonSimUtils.get_active_sim_info(), _AutosaveHandler._get_autosave_interval(), _AutosaveHandler._time_to_save, repeating=True, cross_zone=True)
        if not has_setup_alarm_before:
            CommonBasicNotification(
                'S4ASM Autosaving Setup',
                'S4ASM will autosave every {} minutes real time. Look for the notification!'.format(_AutosaveHandler._AUTOSAVE_INTERVAL_MINUTES)
            ).show()


@CommonIntervalEventRegistry.run_every(ModInfo.get_identity(), milliseconds=5000)
def _register_autosave_alarm() -> None:
    _AutosaveHandler._register_alarm()


@Command('s4asm.autosave', command_type=CommandType.Live)
def _s4asm_perform_autosave(_connection: int=None):
    try:
        output = CheatOutput(_connection)
        output('Attempting to perform autosave.')
        if _AutosaveHandler._time_to_save():
            output('Done doing autosave.')
        else:
            output('ERROR: Failed to autosave.')
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'An exception occurred while autosaving.', exception=ex)
