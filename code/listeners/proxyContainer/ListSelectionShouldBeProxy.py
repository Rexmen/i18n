from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ListSelectionShouldBeProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'expected'])] = self
        #Verify selection list `locator` has `expected` options selected.
        # selection list 在網頁中: <select>
    def i18n_Proxy(self, func):
        def proxy(self, locator, *expected):
            ListSelectionShouldBeProxy.show_warning(self, locator)
            # for expected_selection in len(*expected):
            #     possible_translation = i18n.I18nListener.MAP.value(expected_selection)
            options = self._get_selected_options(locator)
            labels = self._get_labels(options)
            values = self._get_values(options)
            if sorted(expected) not in [sorted(labels), sorted(values)]:
                return func(self, locator, expected)
            # locator_translation = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(value))

            # expected_translation = i18n.I18nListener.MAP.values(expected)
            expected_translation = ""
            for i in i18n.I18nListener.MAP.values(expected):
                expected_translation += ''.join(i)
            # logger.warn(expected_translation)
            return func(self, locator, expected_translation)
        return proxy

    def show_warning(self, locator):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_locator = Proxy().deal_warning_message_for_one_word(locator, 'Locator')
        if message_for_locator != '':
            message = language + test_name + message_for_locator + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)