*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
123
    @{list1} =    Create List    Support    Support    Software
    @{list2} =    Create List    Support    Software    A
    # Log    ${dict1}
    List Should Contain Sub List    ${list1}    ${list2}