*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Remove values from list
    # @{list1} =    Create List    支援    軟體    蘋果
    # Remove Values From List    ${list1}    支援
    @{list1} =    Create List    Support    Software
    Remove Values From List    ${list1}    Support
    Log    ${list1}