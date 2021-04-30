*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    https://ssl-ezscrum.csie.ntut.edu.tw/ezScrum/    Chrome
              ...      AND    Maximize Browser Window
              ...      AND    Wait Until Element Is Visible    //*[@name='userId']
              ...      AND    Input Text     //*[@name='userId']    binchen561
              ...      AND    Input Text    //*[@name='password']    qwer3asdf4
              ...      AND    Click Button    //*[@name='Next']

*** Test Cases ***
Table cell should contain
    Wait Until Element Is Visible    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']    ${shortPeriodOfTime}
    Table Cell Should Contain    //*[contains(@class, 'x-panel-bwrap')]//table    1    2    binchen561(Bing)
    Close Browser