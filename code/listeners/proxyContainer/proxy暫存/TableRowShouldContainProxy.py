from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class TableRowShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'row', 'expected', 'loglevel=TRACE'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, row, expected, loglevel='TRACE'):
            TableRowShouldContainProxy.show_warning(self, locator, expected)
            row_translation = i18n.I18nListener.MAP.value(row)
            expected_translation = i18n.I18nListener.MAP.value(expected)
            locator_translation = i18n.I18nListener.MAP.value(BuiltIn().replace_variables(locator))
            element = self._find_by_row(locator_translation, row_translation, expected_translation, loglevel)
            
            if element is None:
                return func(self, locator, column, expected, loglevel)
            else:
                return func(self, locator_translation, column_translation, expected_translation, loglevel)
        return proxy

    def show_warning(self, locator, expected):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_locator = Proxy().deal_warning_message_for_one_word(locator, 'Locator')
        message_for_expect = Proxy().deal_warning_message_for_one_word(expect, 'Expect')
        if message_for_locator != '' or message_for_expect != '':
            message = language + test_name + message_for_locator + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)