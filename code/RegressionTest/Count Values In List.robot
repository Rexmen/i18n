*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
123
    @{list1} =    Create List    Support    Support    Software
    # Log    ${dict1}
    ${number} =    Count Values In List    ${list1}    Support
    Log    ${number}