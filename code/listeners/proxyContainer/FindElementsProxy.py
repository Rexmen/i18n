from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.remote.webelement import WebElement
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import sys
import ManyTranslations as ui

class FindElementsProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['by=\'id\'', 'value=None'])] = self
        # value是要找的element的locator , by沒有甚麼作用(印出"xpath"?)
    def i18n_Proxy(self, func):
        def proxy(self, by='id', value=None):
            # logger.warn(by)
            if isinstance(value, WebElement):
                return func(self, by, value)
            xpath = ''
            BuiltIn().import_library('SeleniumLibrary')
            #以下的翻譯方法針對的是"xpath內有需要翻譯的文字"
            locator = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(value)) #會呼叫i18nMap的locator(),將xpath傳入,
                #內部會翻譯xpath內的文字部分，並會設定multiple_translation_words，讓下一行get_multiple_translation_words()取用
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words() 
            # logger.warn(locator)
            is_actual = False
            if len(locator) > 1:
                # logger.warn(multiple_translation_words)
                i18n.I18nListener.Is_Multi_Trans = True
                word_translation = i18n.I18nListener.MAP.values(multiple_translation_words)
                ui.add_translations(multiple_translation_words, word_translation)
                for i, translation_locator in enumerate(locator):
                    xpath += '|' + translation_locator.replace('xpath:', '') if i != 0 else translation_locator.replace('xpath:', '')
                    is_actual = BuiltIn().run_keyword_and_return_status('Get WebElement', translation_locator)
                    if is_actual:
                        actual_locator_message = "System use the locator:'%s' to run!\n" %translation_locator
                        logger.info(actual_locator_message)
            else:
                xpath = locator[0]
            FindElementsProxy.show_warning(self, xpath, value, multiple_translation_words) # if Exist multiple translations of the word show warning
            return func(self, by, BuiltIn().replace_variables(xpath))
        return proxy
    
    def show_warning(self, xpath_with_or, locator, multiple_translation_words):
        if '|' in  xpath_with_or:
            language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
            message_value = 'Multiple translations of the word:\'%s\'' %" ".join(multiple_translation_words)
            test_name = BuiltIn().get_variable_value("${TEST NAME}")
            message = language + 'Test Name: ' + test_name + '\n   ' + 'locator: ' + locator + '\n   ' + message_value + '\n\n' + 'You should verify translation is correct!'
            for multiple_translation_word in multiple_translation_words:
                if multiple_translation_word not in i18n.I18nListener.Not_SHOW_WARNING_WORDS:
                    logger.warn(message)
                    Screenshot().take_screenshot(width=700)