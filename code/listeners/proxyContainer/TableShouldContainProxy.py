from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class TableShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'expected', 'loglevel=\'TRACE\''])] = self
        # TableHeaderShouldContain & TableFooterShouldContain 也適用此keyword
    def i18n_Proxy(self, func):
        def proxy(self, locator, expected, loglevel='TRACE'):
            TableShouldContainProxy.show_warning(self, locator, expected)
            expected_translation = i18n.I18nListener.MAP.value(expected)
            logger.warn(expected_translation)
            # logger.warn("test")
            return func(self, locator, ''.join(expected_translation), loglevel)
        return proxy

    def show_warning(self, locator, expected):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_locator = Proxy().deal_warning_message_for_one_word(locator, 'Locator')
        message_for_expect = Proxy().deal_warning_message_for_one_word(expected, 'Expect')
        if message_for_locator != '' or message_for_expect != '':
            message = language + test_name + message_for_locator + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)