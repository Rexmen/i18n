from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class DictionaryShouldContainKeyProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'key', 'msg=None'])] = self
        # DictionaryShouldContainItem內部也會呼叫到此proxy
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, key, msg=None):
            #創出該次呼叫的參數紀錄
            full_args = [str(dictionary), key] #將dictionary轉str, 方便之後資料讀寫

            #翻譯
            #因為dictionary無法直接翻譯，所以拆成keys和values去分別翻譯，回傳值是list
            dict_keys_trans = i18n.I18nListener.MAP.values(list(dictionary.keys()), full_args)
            dict_have_multi_trans  = False
            for dt in dict_keys_trans:
                if len(dt) >1:
                    dict_have_multi_trans  = True
                    break
            key_trans = i18n.I18nListener.MAP.value(key, full_args)

            #遭遇一詞多譯
            if len(key_trans)>1 or dict_have_multi_trans:
                DictionaryShouldContainKeyProxy.show_warning(self, dictionary, key, full_args) #show warning
                #檢查case會pass or fail
                is_pass = False
                if 'not' in func.__name__:
                    if key not in dictionary.keys():
                        is_pass = True
                else:
                    if key in dictionary.keys():
                        is_pass = True
                if is_pass: #pass
                    # 對預計開啟的UI做一些準備
                    i18n.I18nListener.Is_Multi_Trans = True
                    
                    for i, dt in enumerate(dict_keys_trans):
                        if len(dt)>1 and str(full_args)+list(dictionary.keys())[i] not in ui.UI.unique_log: #FIXME dict keys是否要在這邊判斷
                            multi_trans_word = [list(dictionary.keys())[i]]                                # 還是要移交add_translations處理
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_translations(self, multi_trans_word, dt, full_args)
                    if len(key_trans) > 1 and str(full_args)+key not in ui.UI.unique_log:
                        multiple_translation_word = [key]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_translations(self, multiple_translation_word, key_trans, full_args) #將翻譯詞加進等等UI會用到的dictionary中
            #將dictionary 翻譯過後的key合併 
            # 這邊會出錯，因為key要是唯一值， 暫時用原先的key代替
            # dictionary = dict(zip(list(dictionary.keys()), dictionary.values()))         
            #將處理好的翻譯回傳給robot原生keyword
            #FIXME 這邊比較麻煩，之後user選擇key的唯一翻譯後，目前還是只會回傳原本的key值
            # logger.warn(dictionary)
            return func(self, dictionary, key, msg)
        return proxy

    def show_warning(self, dictionary,key, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict_key = Proxy().deal_warning_message_for_list(dictionary.keys(),full_args, 'DICT_KEY')
        message_for_key = Proxy().deal_warning_message_for_one_word(key, full_args,  'KEY')
        if message_for_dict_key or message_for_key:
            message = language + test_name + message_for_dict_key + '\n' + message_for_key + '\n'\
                        'You should verify translation is correct!'
            logger.warn(message)