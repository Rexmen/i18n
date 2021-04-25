*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
123
    &{dict1} =    Create Dictionary    key=Support
    &{dict2} =    Create Dictionary    key=Support
    # Log    ${dict1}
    Dictionaries Should Be Equal    ${dict1}    ${dict2}