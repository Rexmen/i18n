*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    ../self_util.py
# Test Setup    Load Test Data

*** Test Cases ***
Get test case name
    Log    ${TEST_NAME}
    


*** Keywords ***
# Load Test Data
    # ${data}=    Get File    ${TEST_NAME}.txt
    # Set Test Variable    ${data}    ${data}