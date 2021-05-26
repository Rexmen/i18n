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
Select from list by label "Sprint 18"
    Wait Until Element Is Visible    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']    ${shortPeriodOfTime}
    Double Click Element    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']
    Wait Until Element Is Visible    //*[@id='Project_Top_Panel']    ${shortPeriodOfTime}
    Wait Until Element Is Visible    //*[@class='x-tree-node-anchor']//*[normalize-space()='TaskBoard']    ${shortPeriodOfTime}
    Double Click Element    //*[@class='x-tree-node-anchor']//*[normalize-space()='Scrum Report']
    Select Frame    xpath://iframe[@id='remainingWorkReport']
    Select From List By Label    //*[@id='ShowSprint']    Sprint 18
    Sleep    1s
    List Selection Should Be    //*[@id='ShowSprint']    Sprint 18
    Unselect Frame
    Close Browser