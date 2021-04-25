import SeleniumLibrary
import re
import os
import inspect
import json
import sys
from glob import glob
import SeleniumLibrary
from selenium import webdriver
from robot.libraries.Collections import Collections
from SeleniumLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn

class Trigger:

    def __init__(self):
        self.arg_format = {}
        self.set_proxy_func_to_SeleniumLibrary()
    
    def get_func_proxy(self, func):
        args_declaration = self.get_argument_declaration(func) #得出該func的參數宣告部分
        if repr(args_declaration) in list(self.arg_format.keys()):  #如果參數宣告在arg_format這個dict的keys中
            return self.arg_format[repr(args_declaration)].i18n_Proxy(func)  #回傳arg_format中value(是proxy的類別名).i18n_Proxy(func)
        return func #否則回傳原本的func屬性值

    def get_argument_declaration(self, func):
        args = inspect.getfullargspec(func).args[1:]  # [0] is self, get出該func的參數部分去掉self
        defaults = inspect.getfullargspec(func).defaults #get出該func參數的default部分
        varargs = inspect.getfullargspec(func).varargs
        keywords = inspect.getargspec(func).keywords
        if defaults:            #幫args加上default值，如果有的話
            defaults = ['=' + repr(default) for default in defaults]
            defaults = [''] * (len(args) - len(defaults)) + defaults
            args = list(arg[0] + arg[1] for arg in zip(args, defaults))
        if varargs:
            args.append(varargs)
        if keywords:
            args.append(keywords)
        return args

    def set_proxy_func_to_SeleniumLibrary(self):
        import SeleniumLibrary
        keywords = [keyword.replace(' ', '_').lower() for keyword in SeleniumLibrary.SeleniumLibrary().keywords]
        for str_keywords_class in dir(SeleniumLibrary): 
            keywords_class = getattr(locals().get(SeleniumLibrary.__name__), str_keywords_class)
            for str_method in dir(keywords_class):
                # print(str_method.replace(' ', '_').lower())
                if str_method.replace(' ', '_').lower() in keywords: 
                    func = getattr(keywords_class, str_method)
                    if repr(type(func)) == "<class 'function'>":
                        print(keyword(self.get_func_proxy(func)))
                        break
            
        #                 setattr(keywords_class, str_method, keyword(self.get_func_proxy(func)))
    

if __name__ == '__main__':
    Trigger()