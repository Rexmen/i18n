*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
123
    @{list1} =    Create List    Support    Software    Apple
    ${count} =    Get Match Count    ${list1}    S*
    Log    ${count}