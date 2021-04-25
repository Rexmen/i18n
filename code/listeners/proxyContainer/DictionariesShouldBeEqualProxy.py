from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class DictionariesShouldBeEqualProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dict1', 'dict2', 'msg=None', 'values=True'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, dict1, dict2, msg=None, values=True):
            
            # DictionariesShouldBeEqualProxy.show_warning(self, dict1, dict2)
            if 'not' in func.__name__:
                compare = lambda x,y:True if x != y else False
            else:
                compare = lambda x,y:True if x == y else False
            for dict1_key, dict2_key in zip(dict1.keys(), dict2.keys()):
                dict1_translation = i18n.I18nListener.MAP.value(dict1[dict1_key])
                dict2_translation = i18n.I18nListener.MAP.value(dict2[dict2_key])
                if compare(dict1_translation, dict2_translation):
                    dict1[dict1_key] = dict1_translation
                    dict2[dict2_key] = dict2_translation
                    # logger.warn(dict2)
                    return func(self, dict1, dict2, msg, values)
            return func(self, dict1, dict2, msg, values)
        return proxy

    def show_warning(self, dict1, dict2):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict1 = Proxy().deal_warning_message_for_one_word(dict1, 'Dict1')
        message_for_dict2 = Proxy().deal_warning_message_for_one_word(dict2, 'Dict2')
        message = language + test_name + message_for_dict1 + ' '*3 + '\n' + message_for_dict2 + '\n' + 'You should verify translation is correct!'
        if message_for_dict1 != '' or message_for_dict2 != '':
            logger.warn(message)