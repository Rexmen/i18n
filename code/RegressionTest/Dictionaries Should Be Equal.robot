*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Dictionaries should be equal
    &{dict1} =    Create Dictionary    Software=Support
    &{dict2} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionaries Should Be Equal    ${dict1}    ${dict2}