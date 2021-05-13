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
        # 'Page Should Contain Element' 會呼叫此proxy
    def i18n_Proxy(self, func):
        def proxy(self, by='id', value=None):
            # logger.warn(by)
            if isinstance(value, WebElement):
                return func(self, by, value)
            xpath = ''
            # logger.warn(type(value))
            full_args = [value]
            BuiltIn().import_library('SeleniumLibrary')
            #以下的翻譯方法針對的是"xpath內有需要翻譯的文字"
            locator = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(value), full_args) #會呼叫i18nMap的locator(),將xpath傳入,
                #內部會翻譯xpath內的文字部分，並會設定multiple_translation_words，讓下一行get_multiple_translation_words()取用
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words() 
            is_actual = False
            if len(locator) > 1:
                # logger.warn(multiple_translation_words)
                # logger.warn(locator)
                #判斷case會過或fail
                for i, translation_locator in enumerate(locator):
                    xpath += '|' + translation_locator.replace('xpath:', '') if i != 0 else translation_locator.replace('xpath:', '')
                    is_actual = BuiltIn().run_keyword_and_return_status('Get WebElement', translation_locator) #如果畫面上有該翻譯
                    if is_actual: #pass
                        ## 括起來的是新增的翻譯邏輯
                        i18n.I18nListener.Is_Multi_Trans = True
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        word_translation = i18n.I18nListener.MAP.values(multiple_translation_words, full_args)
                        #FIXME multiple_translation_words有沒有可能是複數
                        ui.UI.add_translations(self, multiple_translation_words, word_translation)
                        ##
                        actual_locator_message = "System use the locator:'%s' to run!\n" %translation_locator
                        logger.info(actual_locator_message)
                        # break
            else:
                xpath = locator[0]
            # logger.warn("break will still run this")
            FindElementsProxy.show_warning(self, xpath, value, multiple_translation_words) # if Exist multiple translations of the word show warning
            return func(self, by, BuiltIn().replace_variables(xpath))
        return proxy

    def show_warning(self, xpath_with_or, locator, multiple_translation_words):
        if '|' in  xpath_with_or:
            language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
            test_name = BuiltIn().get_variable_value("${TEST NAME}")
            # multiple_translation_words = list(set(multiple_translation_words))
            for multiple_translation_word in multiple_translation_words:
                message_value = 'Multiple translations of the word:\'%s\'' % multiple_translation_word
                message = language + 'Test Name: ' + test_name + '\n   ' + 'locator: ' + locator + '\n   ' + message_value + '\n\n' + 'You should verify translation is correct!'
                if multiple_translation_word not in i18n.I18nListener.Not_SHOW_WARNING_WORDS:
                    logger.warn(message)
                    Screenshot().take_screenshot(width=700)