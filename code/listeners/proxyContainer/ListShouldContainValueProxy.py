from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ListShouldContainValueProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list_', 'value', 'msg=None'])] = self
        # Fails if the ``value`` is not found from ``list``
    def i18n_Proxy(self, func):
        def proxy(self, list_, value, msg=None):            
            if 'not' in func.__name__:
                compare = lambda x,y:True if x != y else False
            else:
                compare = lambda x,y:True if x == y else False
            # ListShouldContainValueProxy.show_warning(self, list_, value)
            for list_translation in i18n.I18nListener.MAP.values(list_):
                for value_translation in i18n.I18nListener.MAP.value(value):
                    # logger.warn(type(list_translation))
                    if compare(''.join(list_translation), value_translation):
                        list_translation=[]
                        for i in i18n.I18nListener.MAP.values(list_):
                            list_translation += i 
                        logger.warn(list_translation)
                        logger.warn(value_translation)
                        return func(self, list_translation, value_translation, msg)
            return func(self, list_, value, msg)
        return proxy

    def show_warning(self, list_, value):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list = Proxy().deal_warning_message_for_list(list, 'List')
        message_for_value = Proxy().deal_warning_message_for_one_word(value, 'Value')
        if message_for_list != '' and message_for_value != '':
            message = language + test_name + message_for_list + ' '*3 + '\n' + message_for_value + '\n' + 'You should verify translation is correct!'
            logger.warn(message)