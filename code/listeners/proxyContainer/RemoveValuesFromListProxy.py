from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class RemoveValuesFromListProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list_', 'values'])] = self
        # 移除list中所有包含"values"的值 ，若values不存在list中，忽略
    def i18n_Proxy(self, func):
        def proxy(self, list_, *values):
            # RemoveValuesFromListProxy.show_warning(self, list_, values)
            # logger.warn(values)
            values_translation = ()
            for i in i18n.I18nListener.MAP.values(values):
                temp_list=[]
                for j in i:
                    temp_list.append(j)
                # logger.warn(temp_list)
                values_translation += tuple(temp_list)
            # logger.warn(values_translation)

            list_translation = []
            for i in i18n.I18nListener.MAP.values(list_):
                temp_list=[]
                for j in i:
                    temp_list.append(j)
                list_translation += temp_list
            list_.clear()
            list_ += list_translation
            logger.warn(list_)

            for value in values_translation:
                while value in list_:
                    list_.remove(value)
        return proxy

    def show_warning(self, list_, *values):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_values = Proxy().deal_warning_message_for_list(values, 'Values')
        if message_for_values != '':
            message = language + test_name + message_for_values + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)