*** Settings ***
Force Tags    TableShouldContain
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    http:localhost:3000    Chrome
...                    AND    Maximize Browser Window
Test Teardown    Close Browser

*** Test Cases ***
Table should contain "Support"
    ${table} =    Set Variable    //*[@id='i18n-table']
    Wait Until Element Is Visible    ${table}    ${shortPeriodOfTime}
    Table Should Contain    ${table}    Support
    Close Browser

# Table row should contain
    # Wait Until Element Is Visible    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']    ${shortPeriodOfTime}
    # Table Row Should Contain    //*[contains(@class, 'x-panel-bwrap')]//table    1    binchen561(Bing)
    # Close Browser

# Table column should contain
    # Wait Until Element Is Visible    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']    ${shortPeriodOfTime}
    # Table Column Should Contain    //*[contains(@class, 'x-panel-bwrap')]//table    2    binchen561(Bing)
    # Close Browser

# Table cell should contain
    # Wait Until Element Is Visible    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']    ${shortPeriodOfTime}
    # Table Cell Should Contain    //*[contains(@class, 'x-panel-bwrap')]//table    1    2    binchen561(Bing)
    # Close Browser