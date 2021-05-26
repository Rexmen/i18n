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

Dictionary should contain sub dictionary
    &{dict1} =    Create Dictionary    Software=Support    A=B
    &{dict2} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionary Should Contain Sub Dictionary    ${dict1}    ${dict2}