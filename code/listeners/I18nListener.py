import SeleniumLibrary
import inspect
import os
import json
import sys
import itertools
import time
import re
from glob import glob
from selenium import webdriver
from I18nMap import I18nMap
from MappingRoutesGenerator import MappingRoutesGenerator
from SeleniumLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger
from robot.libraries.Screenshot import Screenshot
from selenium.webdriver.remote.webelement import WebElement
from I18nTrigger import I18nTrigger
# from ManyTranslations import run

class I18nListener:
 
    ROBOT_LISTENER_API_VERSION = 2
    MAP = None
    TRANSLATION_FILE = json.loads("{}") # json -> python
    LOCALE = None
    Not_SHOW_WARNING_WORDS = []

    def __init__(self, locale='en-US', not_show_warning_words='None'):
        self.is_admin_language_set=False
        self.is_ui_open=False
        self.locale = locale
        self.attrs = {}
        self.locale_dict = {'en-US':'United Kingdom - English', 
                            'ja':'日本 - 日本語', 
                            'ko':'대한민국 - 한국어', 
                            'zh-CN':'中国 - 简体中文', 
                            'zh-TW':'台灣 - 繁體中文',  
                            'de-CH':'Schweiz - Deutsch'}
        MappingRoutesGenerator().generate()
        for f in glob('%s/languageFiles/%s/*%s.json' % (os.path.dirname(os.path.abspath(__file__)), locale, locale)): #各種語言翻譯檔(common-xx.json more-xx.json etc.)
            with open(f, 'r', encoding='UTF-8') as i18n_file: #將json檔打開
                i18n_dict = json.load(i18n_file)  #將裏頭的json結構轉換成python dict
            self.combine_i18n_dict(source_dict=i18n_dict, target_dict=I18nListener.TRANSLATION_FILE)
        I18nListener.MAP = I18nMap(I18nListener.TRANSLATION_FILE, locale) #i18nMAP，傳入擁有翻譯檔dict的TRANSLATION_FILE 和 語言
        I18nListener.LOCALE = locale # for get language Ex zh-TW, zh-CN
        I18nListener.Not_SHOW_WARNING_WORDS = self.parse_not_show_warning_words(not_show_warning_words)

    '''
        append all key, value of source_dict to target_dict
        source_dict is the dict of json file like 'common-zh-TW.json'...
    '''
    def combine_i18n_dict(self, source_dict, target_dict): #寫一份到TRANSLATION_FILE
        for key, value in source_dict.items():
            target_dict[key] = value
    
    def start_suite(self, name, attrs):
        if not self.is_admin_language_set:#set the admin language in the first suite start
            self.is_admin_language_set=True
            BuiltIn().set_global_variable('${language}',self.locale_dict[self.locale])
    
    def parse_not_show_warning_words(self, words_string):
        if words_string == "Not_show_warning.txt":
            Not_show_warning_txt = glob('%s/Not_show_warning.txt' % (os.path.dirname(os.path.abspath(__file__))))[0]
            with open(Not_show_warning_txt, 'r', encoding='utf-8') as f:
                words_string = f.read()
        words = words_string.split('+')
        return words

    def end_suite(self, name, attrs):
        if not self.is_ui_open:
            self.is_ui_open=True
            import ManyTranslations
            ManyTranslations.run()