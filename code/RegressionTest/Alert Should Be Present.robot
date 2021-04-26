*** Settings ***
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    Dialogs
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_alert    ${browser}
...                    AND    Maximize Browser Window
Test Teardown    Close Browser

*** Test Cases ***
123
    Select Frame    xpath://iframe[@id='iframeResult']
    Click Element After It Is Visible    //*[normalize-space() = 'Try it']
    Alert Should Be Present    Support
    Unselect Frame