from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ShouldContainProxy(Proxy):   #container要包含item才算pass
    def __init__(self, arg_format):
        arg_format[repr(['container', 'item', 'msg=None', 'values=True', 'ignore_case=False'])] = self
                        # container:一個腳本自定義的list([support, supply...]), item:腳本傳入的item(support)
    def i18n_Proxy(self, func):
        def proxy(self, container, item, msg=None, values=True, ignore_case=False):
            logger.warn("fuck should contain")
            ShouldContainProxy.show_warning(self, container, item)  #因為存在一詞多譯，所以呼叫show_warning
            for translation_container in i18n.I18nListener.MAP.values(container): #對container裡的物件做map
                for translation_item in i18n.I18nListener.MAP.value(item): #對item做map
                    if translation_item in translation_container: # if 支援 in [支援服務, 提供...]
                                                                  # if 支援服務 in 
                        return func(self, translation_container, translation_item, msg, values, ignore_case)
            return func(self, container, item, msg, values, ignore_case)
        return proxy
    
    def show_warning(self, container, item):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_container = Proxy().deal_warning_message_for_list(container, 'container')
        message_for_item = Proxy().deal_warning_message_for_one_word(item, 'Expected Contain')
        if message_for_container != '' or message_for_item != '':
            message = language + test_name + message_for_container + ' '*3 + '\n' +  message_for_item + '\n' + 'You should verify translation is correct!'
            logger.warn(message)