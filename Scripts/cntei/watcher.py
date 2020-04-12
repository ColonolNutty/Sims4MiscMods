import os
import sims4.tuning.serialization
from sims4communitylib.services.common_service import CommonService
from cntei.modinfo import ModInfo
from sims4.collections import make_immutable_slots_class
from sims4.commands import Command, CommandType, CheatOutput
from sims4.localization import LocalizationHelperTuning
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_utils import CommonLogUtils
from ui.ui_dialog import ButtonType, UiDialogOkCancel, UiDialogResponse
from ui.ui_dialog_notification import UiDialogNotification
import datetime
import html


# Classes for the error dialog or notification
# noinspection PyMissingOrEmptyDocstring,PyAttributeOutsideInit
class ErrorDialog(UiDialogOkCancel):
    def show_dialog(self, **kwargs):
        self.title =  lambda **_: LocalizationHelperTuning.get_raw_text('Tuning Error Notifier')
        self.text = lambda **_: LocalizationHelperTuning.get_raw_text('XML tuning errors matching your filters were detected.  Press OK to view these in your web browser, or Cancel to ignore.')
        super().show_dialog(**kwargs)


# noinspection PyMissingOrEmptyDocstring,PyAttributeOutsideInit
class ErrorNotification(UiDialogNotification):
    def show_dialog(self, **kwargs):
        self.title = lambda **_: LocalizationHelperTuning.get_raw_text('Tuning Error Notifier')
        self.text = lambda **_: LocalizationHelperTuning.get_raw_text('XML tuning errors matching your filters were detected.  Press the Report button below to view these in your web browser.')
        # noinspection PySetFunctionToLiteral
        response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'tuning_notifier.report'})
        response = UiDialogResponse(dialog_response_id=ButtonType.DIALOG_RESPONSE_OK, ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND, response_command=response_command, text=lambda **_: LocalizationHelperTuning.get_raw_text('Report'))
        self.ui_responses = (response,)
        super().show_dialog(**kwargs)


# The main tuning watcher class.  Any tuning errors that match one of the strings in the filter_text list
# are stored in a dict for later reporting.
# noinspection PyMissingOrEmptyDocstring,PyAttributeOutsideInit
class TuningWatcher(CommonService):
    _instance = None
    _type = None
    _name = None
    _log_entries = {}
    _alert_ran = False

    # Store options passed by the package __init__
    def set_filters(self, filter_text, exclude_text, use_dialog):
        self._filter_text = [txt.lower() for txt in filter_text]
        self._exclude_text = [txt.lower() for txt in exclude_text]
        self._use_dialog = use_dialog

    # Called by the tuning serialization to store what tuning instance is currently being loaded.
    def set_instance(self, instance, type_loaded, name):
        self._instance = instance
        self._type = type_loaded
        self._name = name

    # Called by the patched Logger.error() method and checks to see if the message contains
    # any of the filter_text strings.  If so, the message is stored for later reporting.
    def process_log_message(self, message, *args):
        if self._name and [True for txt in self._filter_text if txt in self._name.lower()] and not [True for txt in self._exclude_text if txt in self._name.lower()]:
            msg = message.format(*args)
            if self._name not in self._log_entries:
                self._log_entries[self._name] = []
            self._log_entries[self._name].append(msg)

    # Called by the zone loading completion injected in the package __init__
    def errors_alert(self):
        if self._alert_ran:
            return

        def dialog_callback(_dialog):
            if _dialog.response == ButtonType.DIALOG_RESPONSE_OK:
                self.generate_report()

        if len(self._log_entries) > 0:
            if self._use_dialog:
                dialog = ErrorDialog(None).TunableFactory().default(None)
                dialog.show_dialog(on_response=dialog_callback)
            else:
                notification = ErrorNotification(None).TunableFactory().default(None)
                notification.show_dialog()
        self._alert_ran = True

    # Generates the HTML report in a temporary file.  This is called from the dialog_callback
    # or the notification button's cheat command.  A callback is registered to be called at Python
    # exit time to remove the temporary file.
    def generate_report(self):
        file_path = CommonLogUtils.get_message_file_path(ModInfo.get_identity().base_namespace)
        dir_name = os.path.dirname(file_path)
        file_path = os.path.join(dir_name, ModInfo.get_identity().base_namespace + '_results.html')
        try:
            opened_file = open(file_path, mode='a', buffering=1, encoding='utf-8')
            opened_file.write('<html><head><title>Tuning Error Notifier Results</title><body>')
            opened_file.write('<center><font size="+3" color="#E00000">Tuning Error Notifier Report<br></font><font size="+1" color="#C00000">{}</font></center><p>'.format(datetime.datetime.now().strftime('%c')))
            for name in self._log_entries:
                opened_file.write('<h3><font color="#0000ff">{}</font></h3>'.format(html.escape(name)))
                opened_file.write('<ul>')
                for msg in self._log_entries[name]:
                    opened_file.write('<li>{}</li>'.format(html.escape(msg).replace(' ', '&nbsp;')))
                opened_file.write('</ul>')
            opened_file.write('</body></html>')
            opened_file.flush()
            opened_file.close()
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Problem occurred when generating error report.', exception=ex)
            return False


# Cheat command to be called by the UI notification if the Report button is pressed.
@Command('tuning_notifier.report', command_type=CommandType.Live)
def _cntei_generate_error_report(_connection=None):
    output = CheatOutput(_connection)
    output('Generating tuning error report.')
    TuningWatcher.get().generate_report()
    output('Finished generating tuning error report.')


_original_load_from_xml = sims4.tuning.serialization.load_from_xml


def _load_from_xml(resource_key, resource_type, inst, from_reload=False):
    TuningWatcher.get().set_instance(resource_key.instance, resource_type, inst.__name__)
    return _original_load_from_xml(resource_key, resource_type, inst, from_reload=from_reload)


sims4.tuning.serialization.load_from_xml = _load_from_xml
