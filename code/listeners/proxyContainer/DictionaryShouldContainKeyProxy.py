from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class DictionaryShouldContainKeyProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'key', 'msg=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, key, msg=None):
            if not dictionary or not key:
                return func(self, dictionary, key, value, msg)
            if 'not' in func.__name__:
                compare = lambda x,y:True if x != y else False
            else:
                compare = lambda x,y:True if x == y else False
            DictionaryShouldContainKeyProxy.show_warning(self, dictionary)
            trans_key = i18n.I18nListener.MAP.value(key)

            for dict_key in dictionary.keys():
                dict_trans_key = i18n.I18nListener.MAP.value(dict_key)
                dict_trans_value = i18n.I18nListener.MAP.value(dictionary[dict_key])
                logger.warn(dict_trans_key)
                if compare(dict_trans_key, trans_key):
                    new_dict = {}
                    new_dict[''.join(dict_trans_key)] = ''.join(dict_trans_value)
                    logger.warn(new_dict)
                    return func(self, new_dict, ''.join(trans_key), msg)
            return func(self, dictionary, key, msg)
        return proxy

    def show_warning(self, dictionary):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict = Proxy().deal_warning_message_for_one_word(dict, 'DICT')
        if message_for_dict != '':
            message = language + test_name + message_for_dict + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)