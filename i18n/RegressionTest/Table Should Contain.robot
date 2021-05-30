*** Settings ***
Force Tags    TableShouldContain
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    http://localhost:3000    Chrome
...                    AND    Maximize Browser Window
Test Teardown    Close Browser

*** Test Cases ***
Table should contain "Support"
    ${table} =    Set Variable    //*[@id='i18n-table']
    Wait Until Element Is Visible    ${table}    ${shortPeriodOfTime}
    Table Should Contain    ${table}    Support

Table row should contain "Support"
    ${table} =    Set Variable    //*[@id='i18n-table']
    Wait Until Element Is Visible    ${table}    ${shortPeriodOfTime}
    Table Row Should Contain    ${table}    1    Support

Table column should contain "Support"
    ${table} =    Set Variable    //*[@id='i18n-table']
    Wait Until Element Is Visible    ${table}    ${shortPeriodOfTime}
    Table Column Should Contain    ${table}    3    Support
    Close Browser

Table cell should contain "Support"
    ${table} =    Set Variable    //*[@id='i18n-table']
    Wait Until Element Is Visible    ${table}    ${shortPeriodOfTime}
    Table Cell Should Contain    ${table}    1    3    Support
    Close Browser