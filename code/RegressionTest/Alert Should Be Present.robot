*** Settings ***
Library    Dialogs
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    http://www.takka.com.hk/jstutor/ch3/ch3.htm#3.1    ${browser}
...                    AND    Maximize Browser Window
# Test Teardown    Close Browser

*** Test Cases ***
123
    # Select Frame    xpath://iframe[@id='iframeResult']
    Click Element After It Is Visible    //a[normalize-space()='alert1.htm']
    # Alert Should Be Present    看到這處覺得怎樣? 請按一下繼續
    # Input Text Into Alert    hello test!
    # Unselect Frame