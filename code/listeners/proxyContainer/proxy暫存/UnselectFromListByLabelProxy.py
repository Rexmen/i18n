from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class UnselectFromListByLabelProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', '*labels'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, *labels)
            if not labels:
                return func(self, locator, labels)
            UnselectFromListByLabelProxy.show_warning(self, labels)
            labels_translation = i18n.I18nListener.MAP.values(labels)
            return func(self, locator, labels_translation)
        return proxy

    def show_warning(self, labels):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_labels = Proxy().deal_warning_message_for_list(label, 'Label')
        if message_for_locator != '':
            message = language + test_name + message_for_labels + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)