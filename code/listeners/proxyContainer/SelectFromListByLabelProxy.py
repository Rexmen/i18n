from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class SelectFromListByLabelProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'labels'])] = self
    # select options from selection list by labels
    # UnselectFromListByLabel 也適用此方法， 但unselect僅能用在multi-selections
    def i18n_Proxy(self, func):
        def proxy(self, locator, *labels):
            if not labels:
                return func(self, locator, labels)
            SelectFromListByLabelProxy.show_warning(self, locator)
            # locator_translation = i18n.I18nListener.MAP.value(BuiltIn().replace_variables(locator))

            labels_translation = ""
            for i in i18n.I18nListener.MAP.values(labels):
                labels_translation += ''.join(i)
            logger.warn(labels_translation)
            return func(self, locator, labels_translation)
        return proxy

    def show_warning(self, locator):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_locator = Proxy().deal_warning_message_for_one_word(locator, 'Locator')
        if message_for_locator != '':
            message = language + test_name + message_for_locator + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)