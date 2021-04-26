from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class RemoveFromDictionaryProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'keys'])] = self
        #Remove given keys from the dictionary if key not in it, ignore it.
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, *keys):
            # RemoveFromDictionaryProxy.show_warning(self, keys)
            have_key = False
            new_dict = {}
            for key in keys:
                if key in dictionary:
                    have_key = True
                    for dict_key in dictionary.keys():
                        dict_key_translation = ''.join(i18n.I18nListener.MAP.value(dict_key))
                        dict_value_translation = ''.join(i18n.I18nListener.MAP.value(dictionary[dict_key]))
                        # logger.warn(dict_key_translation)
                        new_dict.setdefault(dict_key_translation, dict_value_translation)
                    break
            if have_key:
                keys_translation = ()
                for i in i18n.I18nListener.MAP.values(keys):
                    temp=""
                    temp_list=[]
                    for j in i:
                        temp += j
                    temp += ","
                    temp_list = list(temp.split(','))
                    # logger.warn(temp_list)
                    keys_translation += tuple(temp_list[0:-1])                 
                dictionary.clear()
                dictionary.update(new_dict)
                logger.warn(dictionary)
                logger.warn(keys_translation)
                logger.warn(keys)
                return func(self, dictionary, keys_translation) #值不會刪掉 FIXME
            else:   
                return func(self, dictionary, keys)        
        return proxy

    def show_warning(self, *keys):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_keys = Proxy().deal_warning_message_for_list(keys, 'Keys')
        if message_for_keys != '':
            message = language + test_name + message_for_keys + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)