from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class AlertShouldBePresentProxy(Proxy):  #驗證alert資訊有成功出現
    def __init__(self, arg_format):
        arg_format[repr(['text=\'\'', 'action=ACCEPT', 'timeout=None'])] = self
                        # text: 腳本輸入的預期文字(support)
    def i18n_Proxy(self, func):
        def proxy(self, text='', action=ACCEPT, timeout=None):
            logger.warn("fuck alert2")
            possible_translations = i18n.I18nListener.MAP.value(text) #support可能有多種翻譯
            if len(possible_translation) > 1:
                AlertShouldBePresentProxy.show_warning(self, text) #因為存在一詞多譯，所以呼叫show_warning
            translation_text = possible_translations[0]
            return func(self, translation_text, action, timeout) #回傳翻譯過後的字給原本的keyword
        return proxy

    def show_warning(self, text):
        language = 'i18n in %s:\n' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_text = Proxy().deal_warning_message_for_one_word(text, 'Text')
        if message_for_text != '':
            message = language + test_name + message_for_text + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)

