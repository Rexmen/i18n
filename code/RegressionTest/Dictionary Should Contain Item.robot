*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
123
    &{dict1} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionary Should Contain Item    ${dict1}    Software    Support

Dictionary should contain key
    &{dict1} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionary Should Contain Key    ${dict1}    Software

Dictionary should contain value
    &{dict1} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionary Should Contain Value    ${dict1}    Support

Dictionary should not contain key
    &{dict1} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionary Should Not Contain Key    ${dict1}    test

Dictionary should not contain value
    &{dict1} =    Create Dictionary    Software=Support
    # Log    ${dict1}
    Dictionary Should Not Contain Value    ${dict1}    test

Dictionary should contain sub dictionary
    &{dict1} =    Create Dictionary    Software=Support    A=B
    &{dict2} =    Create Dictionary    Software=Support    A=B
    # Log    ${dict1}
    Dictionary Should Contain Sub Dictionary    ${dict1}    ${dict2}