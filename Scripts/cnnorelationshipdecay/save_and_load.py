import os
from typing import Any, Type

from cnnorelationshipdecay.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_early_load import S4CLZoneEarlyLoadEvent
from sims4communitylib.events.zone_spin.events.zone_save import S4CLZoneSaveEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils
from sims4communitylib.utils.common_log_utils import CommonLogUtils


class NRDSettings:
    """ Settings used by NRD. """
    FRIENDSHIP_DECAY = 'nrd_friendship_decay'
    ROMANCE_DECAY = 'nrd_romance_decay'


class NRDSettingUtils(CommonService, HasLog):
    """ Handles Json Data for NRD. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'nrd_setting_io_utils'

    def __init__(self) -> None:
        super().__init__()
        self.save_data = dict()
        self.settings = None
        self.has_loaded = False

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=dict())
    def load(self) -> bool:
        """ Load settings. """
        file_path = self._get_file_name()
        try:
            self.save_data = CommonJSONIOUtils.load_from_file(file_path)
            self.has_loaded = True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while loading settings.', exception=ex)
        self._setup()
        return True

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def save(self) -> bool:
        """ Save settings. """
        file_path = self._get_file_name()
        return CommonJSONIOUtils.write_to_file(file_path, self.save_data)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def _setup(self) -> None:
        if self.save_data is None:
            self.save_data = dict()
        if NRDSettings.FRIENDSHIP_DECAY not in self.save_data:
            self.save_data[NRDSettings.FRIENDSHIP_DECAY] = 100
        if NRDSettings.ROMANCE_DECAY not in self.save_data:
            self.save_data[NRDSettings.ROMANCE_DECAY] = 100

    def get_setting(self, setting_name: str, variable_type: Type) -> Any:
        return variable_type(self.save_data[setting_name])

    def set_setting(self, setting_name: str, value: Any) -> Any:
        self.save_data[setting_name] = value

    def _get_file_name(self) -> str:
        return os.path.join(self._get_save_dir(), 'cnnorelationshipdecay.json')

    def _get_save_dir(self) -> str:
        return os.path.join(CommonLogUtils.get_sims_documents_location_path(), 'saves', 'CNNoRelationshipDecay')


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _nrd_on_zone_late_load(event_data: S4CLZoneEarlyLoadEvent) -> bool:
    return NRDSettingUtils().load()


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _nrd_on_zone_save(event_data: S4CLZoneSaveEvent) -> bool:
    return NRDSettingUtils().save()
