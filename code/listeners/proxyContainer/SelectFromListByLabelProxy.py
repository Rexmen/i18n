from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from SeleniumLibrary.keywords.selectelement import SelectElementKeywords

class SelectFromListByLabelProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'labels'])] = self
    # select options from selection list by labels
    # UnselectFromListByLabel 也適用此方法， 但unselect僅能用在multi-selections
    def i18n_Proxy(self, func):
        def proxy(self, locator, *labels):
            if not labels:                          #檢查機制
                return func(self, locator, labels)
            #創出該呼叫的參數紀錄
            full_args = [locator, str(labels)]

            BuiltIn().import_library('SeleniumLibrary')
            #翻譯， 會翻譯xpath內有需要被翻譯的屬性(邏輯定義在i18nMap)，翻譯完需要屬性後會回傳整條xpath，
            #並會設定multiple_translation_words，讓下一行get_multiple_translation_words()取用
            locator_trans = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(locator), full_args)
            # logger.warn(locator_trans)
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words()
            words_trans = i18n.I18nListener.MAP.values(multiple_translation_words, full_args)

            labels_trans = i18n.I18nListener.MAP.values(labels, full_args)
            labels_have_multi_trans = False
            for lt in labels_trans:
                if len(lt) >1:
                    labels_have_multi_trans = True
                    break

            xpath = ""
            #遭遇一詞多譯
            if len(locator_trans)>1 or labels_have_multi_trans:
                SelectFromListByLabelProxy.show_warning(self, multiple_translation_words, labels, full_args) #show warning
                #對翻譯過後可能的多種xpath做串接
                for i, lt in enumerate(locator_trans):
                    xpath += '|' + locator_trans.replace('xpath', '') if i!=0 else locator_trans.replace('xpath', '')

                #判斷原本case會過還是fail (使用原生library)
                all_options = SelectElementKeywords._get_options(self, locator)
                all_labels = SelectElementKeywords._get_labels(all_options)
                
                if sorted(labels) in [sorted(all_labels)]: # pass
                    # 對預計開啟的UI做一些準備
                    i18n.I18nListener.Is_Multi_Trans = True
                    ui.UI.origin_xpaths_or_arguments.append(full_args)
                    for i, word_trans in enumerate(words_trans):
                        if len(word_trans)>1 and multiple_translation_words[i] not in ui.UI.translations_dict.keys():
                            multi_trans_word = [multiple_translation_words[i]]                                
                            ui.UI.add_translations(self, multi_trans_word, word_trans)
                    for i, lt in enumerate(labels_trans):
                        if len(lt) > 1 and labels[i] not in ui.UI.translations_dict.keys():
                            multi_trans_word = [labels[i]]     
                            ui.UI.add_translations(self, multi_trans_word, lt) #將翻譯詞加進等等UI會用到的dictionary中
            else: #沒有一詞多譯
                xpath = locator_trans[0]
            #將處理好的翻譯回傳給robot原生keyword
            #這邊labels是tuple可以用'*' unpack argument，但labels_trans內部item還是list
            #為了下面回傳時好處理，此處必須把list包list的一詞多譯壓縮成一個string
            newlt = ""
            for lt in labels_trans:
                for single_tran in lt:
                    newlt += single_tran + " " 
                    # FIXME 這邊是應急的處理，實際上一詞多譯應該是[x,x]分開的
                    # 且此處理會導致選不到畫面上的option
                    # 應該想辦法把所有可能的翻譯詞都切開來
            labels_trans = [newlt[:-1]] #此作法的缺點是可能會有存在畫面上不存在的option
            # logger.warn(expected_trans)
            return func(self, BuiltIn().replace_variables(xpath), *tuple(labels_trans))
        return proxy

    def show_warning(self, multi_trans_words, labels, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_words = Proxy().deal_warning_message_for_list(multi_trans_words,full_args, 'MULTI_TRANS_WORDS')
        message_for_labels = Proxy().deal_warning_message_for_list(labels, full_args, 'LABELS')
        if message_for_words or message_for_labels:
            message = language + test_name + message_for_words + '\n' + \
                message_for_labels + '\n' +'You should verify translation is correct!'
            logger.warn(message)