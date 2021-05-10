*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Count values in list
    @{list1} =    Create List    Support    Software
    ${number} =    Count Values In List    ${list1}    Support
    Log    ${number}