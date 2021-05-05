from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import I18nListener as i18n
import json
import re
import os
from glob import glob

class I18nMap:

    def __init__(self, translation_file,locale='en-US'):
        self.locale = locale #language
        self.translation_file = translation_file #i18ntranslation dict(在之前已把json格式翻譯檔轉成了python dictionary)
        self.translation_mapping_routes = self.read_translation_mapping_routes() #存入mappingRoutes.json裡面的資料
        self.multiple_translation_words = []

    def read_translation_mapping_routes(self):
        json_path = glob('%s/mappingRoutes.json' % (os.path.dirname(os.path.abspath(__file__))))[0]
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f) # json -> python
    
    def is_exist_multiple_translation_words(self, text):
            if len(self.value(text)) > 1: #跑value()，看看翻譯是否大於一個
                self.multiple_translation_words.append(text) 
    
    '''
        new_locate_rule -> key should be the regular expression rule
                           I will use findall to find the word that is needed to translate .
                           so value should be the your match word group position.
    '''
    def locator(self, xpath, new_locate_rule={}): #會被某些需要翻譯locator的proxy呼叫
        def combine_locate_rule(locate_rule):  
            default_rule = {
                    '((text|normalize-space)\((text\(\))?\) ?= ?(\'|\")(([0-9a-zA-Z.?&()]| )+)(\'|\"))': 4,
                    '((text|normalize-space)\((text\(\))?\)\, ?(\'|\")(([0-9a-zA-Z.?&()]| )+)(\'|\"))': 4,
                    '((@title) ?= ?(\'|\")(([0-9a-zA-Z.?&()]| )+)(\'|\"))' : 3,
                    '((@title), ?(\'|\")(([0-9a-zA-Z.?&()]| )+)(\'|\"))' : 3
                }
            if len(new_locate_rule):
                temp = dict(default_rule.items() + new_locate_rule.items())
                locate_rule = temp
            else:
                locate_rule = default_rule
            return locate_rule

        def find_all_match_word(xpath, locate_rule):  
            all_match_words = {}
            for rule in locate_rule.keys():
                matches = re.findall(rule, xpath)
                all_match_words[rule] = matches
            return all_match_words
        #從這行開始讀
        self.multiple_translation_words = []    
        if not isinstance(xpath, str): #測看看xpath是不是string
            return [xpath]
        translated_xpath = [xpath]
        locate_rule = combine_locate_rule(new_locate_rule) #如果有new rule，會回傳default+新rule，否則回傳default
        all_match_words = find_all_match_word(xpath, locate_rule) #將xpath和rule傳入找所有符合字詞
        for rule, matches in all_match_words.items(): #rule是key, matches是value 
            for match in matches:
                match_group = locate_rule[rule]
                quot_group = match_group - 1 
                self.is_exist_multiple_translation_words(match[match_group])
                translated_xpath = self.translate(match=match[match_group], quot=match[quot_group], xpaths=translated_xpath) # group 0 as self, group 4 as match, group 3 as quot 
        if xpath != list(translated_xpath)[0] :
            self.log_translation_info(xpath, translated_xpath)
        return translated_xpath
    
    def log_translation_info(self, xpath, translated_xpath):
        def is_need_to_show_warning():
            for multiple_translation_word in self.multiple_translation_words:
                if multiple_translation_word in i18n.I18nListener.Not_SHOW_WARNING_WORDS: #circular include 問題
                    return False
            return True   
        
        def deal_translated_xpath_info(translated_xpath):
            translated_xpath_info = ''
            for i,temp_xpath in enumerate(translated_xpath):
                temp = str(i+1) + '. ' + temp_xpath + '\n   '
                translated_xpath_info = translated_xpath_info + temp
            message = 'Detail Information\ni18n in %s :\nOriginal Locator:\n   1. %s\nTranslated Locator:\n   %s' % (self.locale, xpath, translated_xpath_info)
            return message
        
        warning_or_not = is_need_to_show_warning()
        message = deal_translated_xpath_info(translated_xpath)
        if warning_or_not == False:
            words = ', '.join(self.multiple_translation_words)
            message = message + '\nYou had resolved the multiple translations of the word: \'%s\'' %(words)
        logger.info(message)

    def get_multiple_translation_words(self):
        return self.multiple_translation_words

     # Our target is "XXX" if without quot that it will translate the wrong target.
    def translate(self, match, quot, xpaths):
        origin = quot + match + quot
        translate_list = []
        for translation in self.value(match):
            value = quot + translation + quot
            for xpath in xpaths:
                translate_list.append(xpath.replace(origin, value))
        return list(set(translate_list))

    #For list should be equal, set should be equal...
    def values(self, values):
        return [self.value(v) for v in values]

    def value(self, value):
        try:
            result = self.get_possible_translation(value)
        except (KeyError):
            return [value]
        return list(set(result))

    def get_possible_translation(self, value):
        # 在此處加上判斷，先查看setting是否有value的設定檔，若有則以設定檔為主，否則執行翻譯
        result = []
        if value in i18n.I18nListener.SETTING_TRANS.keys():
            result.append(i18n.I18nListener.SETTING_TRANS[value])
            # logger.warn(result)
            return result
        else:
            try:
                for mapping_route in self.translation_mapping_routes[value]:   #用value當key抓出translation_mapping_routes裡的特定values
                    result.append(eval("self.translation_file%s" % mapping_route))
            except (KeyError):
                raise KeyError
            return result