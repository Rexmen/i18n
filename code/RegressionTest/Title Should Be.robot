*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Resource    ./Keywords.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Title Should Be
    Title Should Be    Microsoft – Official Home Page