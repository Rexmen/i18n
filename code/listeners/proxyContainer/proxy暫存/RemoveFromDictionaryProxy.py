from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class RemoveFromDictionaryProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', '*keys'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, *keys):
            RemoveFromDictionaryProxy.show_warning(self, keys)
            keys_translation = i18n.I18nListener.MAP.values(keys)
            for key in keys:
                if key in dictionary:
                    new_dict = {}
                    for dict_key in dictionary.keys()
                        dict_key_translation = ''.join(i18n.I18nListener.MAP.value(dict_key))
                        dict_value_translation = ''.join(i18n.I18nListener.MAP.value(dictionary[dict_key]))
                        new_dict.setdefault(dict_key_translation, dict_value_translation)
                        return func(self, new_dict, keys_translation)
            return func(self, dictionary, keys)        
        return proxy

    def show_warning(self, *keys):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_keys = Proxy().deal_warning_message_for_list(keys, 'Keys')
        if message_for_keys != '':
            message = language + test_name + message_for_keys + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)