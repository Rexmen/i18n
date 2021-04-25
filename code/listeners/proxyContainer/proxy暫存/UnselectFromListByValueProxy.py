from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class UnselectFromListByValueProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', '*values'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, *values):
            UnselectFromListByValueProxy.show_warning(self, locator)
            if not values:
                return func(self, locator, values)
            values_translation = i18n.I18nListener.MAP.values(values)
            return func(self, locator, values_translation)
        return proxy

    def show_warning(self, locator):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_values = Proxy().deal_warning_message_for_one_word(values, 'Values')
        if message_for_values != '':
            message = language + test_name + message_for_values + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)