*** Settings ***
Force Tags    ElementTextShouldBe
Resource    ../CommonVariables.txt
Resource    ./Keywords.txt
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Test multiple user behavior on microsoft website
    Go To Support Page
    Support Button Text Should Be    Support
    Wait Until Element Is Visible    //*[@id = 'uhfCatLogo' ]//*[normalize-space()='Support']

*** Keywords ***
Support Button Text Should Be
    [Arguments]    ${expected}
    ${supportButton} =    Set Variable    //*[@id = 'uhfCatLogo' ]
    Element Text Should Be    ${supportButton}    ${expected}