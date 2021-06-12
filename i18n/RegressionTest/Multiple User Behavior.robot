*** Settings ***
Force Tags    ElementTextShouldBe
# Resource    ../CommonVariables.txt
Resource    ./Keywords.txt
Library    SeleniumLibrary
# Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Test multiple user behaviors on Microsoft website
    Go To Support Page
    Support Button Text Should Be    Support
    Wait Until Element Is Visible    //*[@id = 'uhfCatLogo' ]//*[normalize-space()='Support']
    Click Element    //*[@id = 'uhfCatLogo' ]//*[normalize-space()='Support']
    ${MicrosoftSupport} =    Set Variable    //*[@id ='supHomeAndLandingPageHeaderContainer']//*[contains(text(), 'Support')]
    ${searchBox} =    Set Variable    //*[@id ='supHomeAndLandingPageSearchBox' and @placeholder ='How can we help you?']
    Sleep    1s
    Page Should Contain Element    ${MicrosoftSupport}
    Page Should Contain Element    ${searchBox}

*** Keywords ***
Support Button Text Should Be
    [Arguments]    ${expected}
    ${supportButton} =    Set Variable    //*[@id = 'uhfCatLogo' ]
    Element Text Should Be    ${supportButton}    ${expected}