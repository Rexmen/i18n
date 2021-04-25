from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class TitleShouldBe(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['title', 'message=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, title, message=None)
            TitleShouldBe.show_warning(self, title)
            title_translation = i18n.I18nListener.MAP.value(title)
            actual = self.get_title()
            if actual != title:
                return func(self, title, message)    
            return func(self, title_translation, message)
        return proxy

    def show_warning(self, title):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_title = Proxy().deal_warning_message_for_one_word(title, 'Title')
        if message_for_title != '':
            message = language + test_name + message_for_title + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)