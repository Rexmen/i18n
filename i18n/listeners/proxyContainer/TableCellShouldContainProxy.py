from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from SeleniumLibrary.keywords.tableelement import TableElementKeywords

class TableCellShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'row', 'column', 'expected', 'loglevel=\'TRACE\''])] = self
        # <table>
    def i18n_Proxy(self, func):
        def proxy(self, locator, row, column, expected, loglevel='TRACE'):
            #創出該呼叫的參數紀錄
            full_args = [locator, row, column, expected]

            #翻譯
            expected_trans = i18n.I18nListener.MAP.value(expected, full_args)
            locator_trans = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(locator), full_args)
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words()
            word_trans = i18n.I18nListener.MAP.values(multiple_translation_words, full_args)

            xpath = ''
            my_expected = ''
            # logger.warn(locator_trans)
            #遭遇一詞多譯            
            if len(expected_trans)>1 or len(locator_trans)>1:
                TableCellShouldContainProxy.show_warning(self, multiple_translation_words, expected, full_args) #show warning

                #檢查case會pass or fail
                for i, lt in enumerate(locator_trans):
                    is_pass = False
                    is_actual = BuiltIn().run_keyword_and_return_status('Get WebElement', lt) #如果畫面上有該翻譯的element存在
                    if is_actual:
                        xpath += lt.replace('xpath:','')
                        content = TableElementKeywords.get_table_cell(self, lt, row, column, loglevel)
                        for et in expected_trans:
                            if et in content:
                                # 因為expected_trans在一詞多譯的情況下可能不只一種，
                                # 直接回傳會導致case出錯，所以目前打算在proxy先測試並取唯一值再回傳
                                my_expected += et
                                is_pass = True
                                break

                    if is_pass: #pass
                        # 對預計開啟的UI做一些準備
                        i18n.I18nListener.Is_Multi_Trans = True
                        
                        for i, wt in enumerate(word_trans):
                            if len(wt)>1 and str(full_args)+multiple_translation_words[i] not in ui.UI.unique_log: #FIXME dict keys是否要在這邊判斷
                                multi_trans_word = [multiple_translation_words[i]]                            # 還是要移交add_translations處理
                                ui.UI.origin_xpaths_or_arguments.append(full_args)
                                ui.UI.add_translations(self, multi_trans_word, wt, full_args)
                        if len(expected_trans) > 1 and str(full_args)+expected not in ui.UI.unique_log:
                            multiple_translation_word = [expected]     
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_translations(self, multiple_translation_word, expected_trans, full_args) #將翻譯詞加進等等UI會用到的dictionary中
                        break
            else: #沒有一詞多譯的情況
                xpath = locator_trans[0].replace('xpath:','')
                my_expected = expected_trans[0]

            #將處理好的翻譯回傳給robot原生keyword
            return func(self, xpath, row, column, my_expected, loglevel)
        return proxy

    def show_warning(self, multiple_translation_words, expected, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_multi_trans_words = Proxy().deal_warning_message_for_list(multiple_translation_words, full_args, 'MULTI_TRANS_WORDS')
        message_for_expected = Proxy().deal_warning_message_for_list(expected, full_args, 'EXPECTED')
        if message_for_multi_trans_words or message_for_expected:
            message = language + test_name + message_for_multi_trans_words + '\n' +\
                      message_for_expected + '\n' + 'You should verify translation is correct!'
            logger.warn(message)