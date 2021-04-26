from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ListShouldContainSubListProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list1', 'list2', 'msg=None', 'values=True'])] = self
    #驗證list2中的所有元件都有被包含在list1中
    def i18n_Proxy(self, func):
        def proxy(self, list1, list2, msg=None, values=True):
            # ListShouldContainSubListProxy.show_warning(self, list1, list2)
            for item2 in list2:
                if item2 not in list1:
                    return func(self, list1, list2, msg, values)
            translation_list1 = i18n.I18nListener.MAP.values(list1)
            logger.warn(translation_list1)
            translation_list2 = i18n.I18nListener.MAP.values(list2)
            return func(self, translation_list1, translation_list2, msg, values)
        return proxy

    def show_warning(self, list1, list2):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list1 = Proxy().deal_warning_message_for_one_word(list1, 'List1')
        message_for_list2 = Proxy().deal_warning_message_for_one_word(list2, 'List2')
        if message_for_list1 != '' and message_for_list2 != '':
            message = language + test_name + message_for_list1 + ' '*3 + '\n' + message_for_list2 + '\n' +'You should verify translation is correct!'
            logger.warn(message)