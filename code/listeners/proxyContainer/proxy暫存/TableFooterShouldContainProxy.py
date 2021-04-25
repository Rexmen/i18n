from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class TableFooterShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'expected', 'loglevel=TRACE'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, expected, loglevel='TRACE')
            TableFooterShouldContainProxy.show_warning(self, locator, expected)
            locator_translation = i18n.I18nListener.MAP.value(BuiltIn().replace_variables(locator))
            expected_translation = i18n.I18nListener.MAP.value(expected)
            element = self._find_by_footer(locator, expected)
            if element is None:
                return func(self, locator, expected, loglevel)
            return func(self, locator_translation, expected_translation, loglevel)
        return proxy

    def show_warning(self, locator, expected):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_locator = Proxy().deal_warning_message_for_one_word(locator, 'Locator')
        message_for_expect = Proxy().deal_warning_message_for_one_word(expect, 'Expect')
        if message_for_locator != '':
            message = language + test_name + message_for_locator + ' '*3 + '\n' + message_for_expect + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)