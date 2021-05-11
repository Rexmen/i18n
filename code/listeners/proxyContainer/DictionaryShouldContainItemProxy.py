from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class DictionaryShouldContainItemProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'key', 'value', 'msg=None'])] = self
        #Dictionary應該包含Item(key : value)
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, key ,value, msg=None):
            logger.warn("HI, this running")
            #定義'比較'的邏輯
            compare = lambda x,y:True if x == y else False
            
            #創出該次呼叫的參數紀錄
            full_args = [str(dictionary), key, value] #將dictionary轉str, 方便之後資料讀寫

            #翻譯
            #因為dictionary無法直接翻譯，所以拆成keys和values去分別翻譯，回傳值是list
            dict_keys_trans = i18n.I18nListener.MAP.values(list(dictionary.keys()), full_args)
            dict_values_trans = i18n.I18nListener.MAP.values(list(dictionary.values()), full_args)            
            whole_trans = []  # 將所有翻譯結果放在一起，用來判斷是否有包含一詞多譯
            whole_trans.append(dict_keys_trans)
            whole_trans.append(dict_values_trans)
            dict_have_multi_trans = False
            for i in range(2):
                for dt in whole_trans[i]: 
                    if len(dt)>1:
                        dict_have_multi_trans = True 
                        break
            key_trans = i18n.I18nListener.MAP.value(key, full_args)
            value_trans = i18n.I18nListener.MAP.value(value, full_args)
            
            #遭遇一詞多譯
            if len(key_trans)>1 or len(value_trans)>1 or dict_have_multi_trans:
                DictionaryShouldContainItemProxy.show_warning(self, dictionary, key, value, full_args) #show warning
                #檢查case會pass or fail
                if key in dictionary.keys() and dictionary[key] == value: #pass
                    # 對預計開啟的UI做一些準備
                    i18n.I18nListener.Is_Multi_Trans = True
                    ui.UI.origin_xpaths_or_arguments.append(full_args)
                    for i, dt in enumerate(dict_keys_trans):
                        if len(dt)>1 and list(dictionary.keys())[i] not in ui.UI.translations_dict.keys(): #FIXME dict keys是否要在這邊判斷
                            multi_trans_word = [list(dictionary.keys())[i]]                                # 還是要移交add_translations處理
                            ui.UI.add_translations(self, multi_trans_word, dt)
                    for i, dt in enumerate(dict_values_trans):
                        if len(dt)>1 and list(dictionary.values())[i] not in ui.UI.translations_dict.keys(): #FIXME dict keys是否要在這邊判斷
                            multi_trans_word = [list(dictionary.values())[i]]                                # 還是要移交add_translations處理
                            ui.UI.add_translations(self, multi_trans_word, dt)
                    if len(key_trans) > 1 and key not in ui.UI.translations_dict.keys():
                        multiple_translation_word = [key]     
                        ui.UI.add_translations(self, multiple_translation_word, key_trans) #將翻譯詞加進等等UI會用到的dictionary中
                    if len(value_trans) > 1 and value not in ui.UI.translations_dict.keys():
                        multiple_translation_word = [value]     
                        ui.UI.add_translations(self, multiple_translation_word, value_trans) #將翻譯詞加進等等UI會用到的dictionary中
            #將dictionary 翻譯過後的key,value合併 
            # 這邊會出錯，因為key要是唯一值， 暫時用原先的key代替
            dictionary = dict(zip(list(dictionary.keys()), dict_values_trans))         
            #將處理好的翻譯回傳給robot原生keyword
            #FIXME 這邊比較麻煩，因為現在key的值是沒有翻譯的狀態，儘管之後user設定唯一翻譯了，這邊還是只會回傳沒翻譯的值
            return func(self, dictionary, key, value_trans)
        return proxy

    def show_warning(self, dictionary,key, value, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict_key = Proxy().deal_warning_message_for_list(dictionary.keys(),full_args, 'DICT_KEY')
        message_for_dict_value = Proxy().deal_warning_message_for_list(dictionary.values(),full_args, 'DICT_VALUE')
        message_for_key = Proxy().deal_warning_message_for_one_word(key, full_args,  'KEY')
        message_for_value = Proxy().deal_warning_message_for_one_word(value, full_args,  'VALUE')
        if message_for_dict_key or message_for_dict_value:
            message = language + test_name + message_for_dict_key + '\n' + message_for_dict_key + '\n' + \
                        message_for_key + '\n' + message_for_value + '\n' +\
                        'You should verify translation is correct!'
            logger.warn(message)