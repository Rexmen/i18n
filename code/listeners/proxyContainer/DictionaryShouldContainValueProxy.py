from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class DictionaryShouldContainValueProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'value', 'msg=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, value, msg=None):
            logger.warn("hi3")
            if not dictionary or not value:
                return func(self, dictionary, value, msg)
            compare = lambda x,y:True if x == y else False
            DictionaryShouldContainValueProxy.show_warning(self, dictionary)
            trans_value = i18n.I18nListener.MAP.value(value)

            for dict_key in dictionary.keys():
                dict_trans_value = i18n.I18nListener.MAP.value(dictionary[dict_key])
                dict_trans_key = i18n.I18nListener.MAP.value(dict_key)
                logger.warn(dict_trans_value)
                if compare(dict_trans_value, trans_value):
                    new_dict = {}
                    new_dict[''.join(dict_trans_key)] = ''.join(dict_trans_value)
                    logger.warn(new_dict)
                    return func(self, new_dict, ''.join(trans_value), msg)
            return func(self, dictionary, value, msg)
        return proxy

    def show_warning(self, dictionary):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict = Proxy().deal_warning_message_for_one_word(dict, 'DICT')
        if message_for_dict != '':
            message = language + test_name + message_for_dict + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)