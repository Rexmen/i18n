from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class GetMatchCountProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list', 'pattern', 'case_insensitive=False', 'whitespace_insensitive=False'])] = self
        #會回傳list中符合pattern的個數
    def i18n_Proxy(self, func):
        def proxy(self, list, pattern, case_insensitive=False, whitespace_insensitive=False):
            if not list or not pattern:
                return func(self, list, pattern, case_insensitive, whitespace_insensitive)
            # GetMatchCountProxy.show_warning(self, list, pattern)
            trans_temp = i18n.I18nListener.MAP.values(list)
            translation_list= []
            for i in trans_temp:
                translation_list += i
            # logger.warn(type(pattern.replace("*", "")))
            translation_pattern = i18n.I18nListener.MAP.value(pattern.replace("*", ""))
            logger.warn(list)
            logger.warn(translation_list)
            logger.warn(''.join(translation_pattern)+"*")
            return func(self, translation_list, ''.join(translation_pattern)+"*", case_insensitive, whitespace_insensitive)
        return proxy

    # def show_warning(self, list, pattern):
    #     language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
    #     test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
    #     message_for_list = Proxy().deal_warning_message_for_list(list, 'List')
        # message_for_pattern = Proxy().deal_warning_message_for_one_word(''.join(pattern), 'Pattern')
        # logger.warn(message_for_list)
        # if message_for_list != '' and message_for_pattern != '':
        #     message = language + test_name + message_for_list + ' '*3 + '\n' + message_for_pattern + '\n' + 'You should verify translation is correct!'
            # logger.warn(message)