from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class TableColumnShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'column', 'expected', 'loglevel=\'TRACE\''])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, column, expected, loglevel='TRACE'):
            TableColumnShouldContainProxy.show_warning(self, locator, expected)
            expected_translation = i18n.I18nListener.MAP.value(expected)
            logger.warn(''.join(expected_translation))
            return func(self, locator, column, ''.join(expected_translation), loglevel)
        return proxy

    def show_warning(self, locator, expected):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_locator = Proxy().deal_warning_message_for_one_word(locator, 'Locator')
        message_for_expected = Proxy().deal_warning_message_for_one_word(expected, 'Expected')
        if message_for_locator != '' or message_for_expected != '':
            message = language + test_name + message_for_locator + ' '*3 + '\n' + message_for_expected + '\n' + 'You should verify translation is correct!'
            logger.warn(message)