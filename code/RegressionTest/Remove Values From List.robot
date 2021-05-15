*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Remove values from list
    @{list1} =    Create List    Support    Software
    Remove Values From List    ${list1}    Support
    List Should Contain Value    ${list1}    軟體
    Log    ${list1}