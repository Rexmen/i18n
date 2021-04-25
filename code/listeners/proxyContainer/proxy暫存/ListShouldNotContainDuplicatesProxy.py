from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ListShouldNotContainDuplicatesProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list_', 'msg=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, list_, msg=None):
            ListShouldNotContainDuplicatesProxy.show_warning(self, list_)
            for item in list_:
                count = list_.count(item)
                if count > 1:
                    return func(self, list_, msg)
            list_translation = i18n.I18nListener.MAP.value(list_)
            return func(self, list_translation, msg)
        return proxy

    def show_warning(self, list_):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list = Proxy().deal_warning_message_for_one_word(list, 'List')
        if message_for_list != '':
            message = language + test_name + message_for_list + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)