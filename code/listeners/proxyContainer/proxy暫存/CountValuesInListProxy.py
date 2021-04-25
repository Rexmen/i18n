from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import sys

class CountValuesInListProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list_', 'value', 'start=0', 'end=None'])] = self
        # 計算list中的指定value之個數
    def i18n_Proxy(self, func):
        def proxy(self, list_, value, start=0, end=None):
            if not list_ or not value:
                return func(self, list_, value, start, end)
            CountValuesInListProxy.show_warning(self, list_, value)
            translation_list = i18n.I18nListener.MAP.values(list_)
            translation_value = i18n.I18nListener.MAP.value(value)            
            return func(self, translation_list, translation_value, start, end)
        return proxy   
    
    def show_warning(self, list_, value):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list = Proxy().deal_warning_message_for_list(list_, 'LIST')
        message_for_value = Proxy().deal_warning_message_for_one_word(value, 'VALUE')
        message = language + test_name + message_for_list + ' '*3 + '\n' + message_for_value + '\n' + 'You should verify translation is correct!' 
        if message_for_list != '' or message_for_value != '':
            logger.warn(message)                        
