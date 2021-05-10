from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class DictionaryShouldContainSubDictionaryProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dict1', 'dict2', 'msg=None', 'values=True'])] = self
        # dict2必須包含於dict1內，否則fail
    def i18n_Proxy(self, func):
        def proxy(self, dict1, dict2, msg=None, values=True):
            compare = lambda x,y:True if x != y else False
            new_dict1={}
            new_dict2={}
            DictionaryShouldContainSubDictionaryProxy.show_warning(self, dict1, dict2)
            for dict2_key in dict2.keys():
                dict2_trans_key = i18n.I18nListener.MAP.value(dict2_key)
                dict2_translation = i18n.I18nListener.MAP.value(dict2[dict2_key])
                for dict1_key in dict1.keys():
                    dict1_trans_key = i18n.I18nListener.MAP.value(dict1_key)
                    dict1_translation = i18n.I18nListener.MAP.value(dict1[dict1_key])
                    # logger.warn(dict1_trans_key)
                    if compare(dict1_translation, dict2_translation) and compare(dict1_key, dict2_key):
                        return func(self, dict1, dict2, msg, values)
                    else :
                        new_dict1[''.join(dict1_trans_key)] = ''.join(dict1_translation)
                        new_dict2[''.join(dict2_trans_key)] = ''.join(dict2_translation)
                        logger.warn(new_dict1)
            return func(self, new_dict1, new_dict2, msg, values)        
        return proxy

    def show_warning(self, dict1, dict2):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict1 = Proxy().deal_warning_message_for_one_word(dict, 'DICT1')
        message_for_dict2 = Proxy().deal_warning_message_for_one_word(dict, 'DICT2')
        if message_for_dict1 != '' and message_for_dict2 != '':
            message = language + test_name + message_for_dict1 + ' '*3 + '\n' + message_for_dict2 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)