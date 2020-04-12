import json
import os
from typing import Dict, Any

from cntei.modinfo import ModInfo
from cntei.watcher import TuningWatcher
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'tei_settings')


class CNTEISettingsLoader:
    _file_name = 'tei_settings'

    @staticmethod
    def load_as_json(file_path):
        if not os.path.isfile(file_path):
            return {}
        with open(file_path, encoding='utf-8') as file:
            return json.loads(file.read())

    @staticmethod
    def load() -> Dict[str, Any]:
        """
            Loads JSON from script_file_path/json_file_name.json
        """
        file_path = CNTEISettingsLoader._get_full_file_path()
        log.format_with_message('Loading JSON data from path', file_path=file_path)
        try:
            result = CNTEISettingsLoader.load_as_json(file_path) or dict()
            log.format_with_message('Load successful.', result=result)
            return result
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to load JSON data from path \'{}\''.format(file_path), exception=ex)
        log.debug('Load failed.')
        return dict()

    @staticmethod
    def _get_full_file_path():
        return os.path.join(CNTEISettingsLoader._get_full_folder_path_of_mod(), '{}.json'.format(CNTEISettingsLoader._file_name))

    @staticmethod
    def _get_full_folder_path_of_mod() -> str:
        root_path = ''
        split_root_path = []
        try:
            root_file = os.path.normpath(os.path.dirname(os.path.realpath(ModInfo.get_identity().file_path))).replace(os.sep, '/')
            log.format(root_file=root_file)
            root_file_split = root_file.split('/')
            end_index = len(root_file_split)
            for i, word in enumerate(root_file_split):
                if str(word).endswith('.ts4script'):
                    end_index = end_index - i
                    break
            for index in range(0, len(root_file_split) - end_index):
                root_path += str(root_file_split[index]) + '/'
                split_root_path.append(root_file_split[index])
            log.format(root_path=root_path, split_root_path=split_root_path)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Problem checking mod installation path', exception=ex)
        return root_path


tei_settings = CNTEISettingsLoader.load()

FILTER_TEXT_LIST = tei_settings.get('filter_text_list', [])                  # A list of strings to search for in instance names to match
EXCLUDE_TEXT_LIST = tei_settings.get('exclude_text_list', [])                  # An optional list of strings to exclude from reporting
USE_DIALOG_ALERT_FOR_ERRORS = tei_settings.get('use_dialog_alert_for_errors', False)     # False alerts with a notification, True will use a modal dialog
REBUILD_INVALID_XML = tei_settings.get('rebuild_invalid_xml', True)              # True patches certain XML load failures with code to rebuild the XML text


TuningWatcher.get().set_filters(FILTER_TEXT_LIST, EXCLUDE_TEXT_LIST, USE_DIALOG_ALERT_FOR_ERRORS)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _cntei_load_outfit_parts_on_zone_load(event_data: S4CLZoneLateLoadEvent):
    if event_data.game_loaded:
        return
    TuningWatcher.get().errors_alert()
