from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class TableCellShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'row', 'column', 'expected', 'loglevel=\'TRACE\''])] = self
        # <table>
    def i18n_Proxy(self, func):
        def proxy(self, locator, row, column, expected, loglevel='TRACE'):
            TableCellShouldContainProxy.show_warning(self, expected)
            expected_translation = i18n.I18nListener.MAP.value(expected)
            logger.warn(''.join(expected_translation))
            return func(self, locator, row, column, ''.join(expected_translation), loglevel)
        return proxy

    def show_warning(self, expected):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_expected = Proxy().deal_warning_message_for_one_word(expected, 'Expected')
        if message_for_expected != '':
            message = language + test_name + message_for_expected + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)