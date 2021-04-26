*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
List should contain value
    @{list1} =    Create List    Software    支援
    # @{list2} =    Create List    Software    支援    支援
    # Log    ${dict1}
    List Should Not Contain Duplicates    ${list1}