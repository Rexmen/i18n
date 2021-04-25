from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class InputTextIntoAlertProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['text', 'action=ACCEPT', 'timeout=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, text, action=ACCEPT, timeout=None):
            if not text:
                return func(self, text, action, timeout)
            InputTextIntoAlertProxy.show_warning(self, text)
            translation_text = i18n.I18nListener.MAP.value(text)
            return func(self, translation_text, action, timeout)
        return proxy

    def show_warning(self, text):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_text = Proxy().deal_warning_message_for_one_word(text, 'Text')
        if message_for_text != '':
            message = language + test_name + message_for_text + '\n' + 'You should verify translation is correct!'
            logger.warn(message)