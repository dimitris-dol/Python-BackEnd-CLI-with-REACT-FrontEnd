
*** Variables ***

${HOSTNAME}             localhost
${PORT}                 8765
${SERVER}               http://${HOSTNAME}:${PORT}/
${BROWSER}              chrome
${username}              teo
${password}             10

*** Settings ***

Documentation   Django Robot Tests
Library         SeleniumLibrary  timeout=10  implicit_wait=0
Library         OperatingSystem
Library         Collections
Library         RequestsLibrary
Library         RequestsChecker
Library         DjangoLibrary  ${HOSTNAME}  ${PORT}  path=C:\users\user\github\front-end-26-2\  manage=manage.py  settings=new.settings
Suite Setup     Start Django and open Browser
Suite Teardown  Stop Django and close Browser


*** Keywords ***

Start Django and open Browser
  Open Browser  ${SERVER}  ${BROWSER}

Stop Django and close browser
  Close Browser
  Stop Django

Input Username
  [Arguments]    ${username}
  Input Text    username    ${username}

Input Password
  [Arguments]    ${password}
  Input Text    password    ${password}

Welcome Page Should Be Open
 Name Should Be    Welcome

 Submit Credentials
    Click Button    submit

*** Test Cases ***

Scenario: As a visitor I can visit the django default page
  Go To  ${SERVER}
  #Wait until page contains element  id=explanation
  #Page Should Contain  It worked!
  #Page Should Contain  Congratulations on your first Django-powered page.
  Input Username    teo
  Input Password    10
  Submit Credentials
  ${data}=  Create Dictionary    username=${username} password=${password}
  Create Session   azure   http://localhost:8765/energy/api
  ${response}=   POST Request    azure    /Login    ${data}
  Check Response Status   ${response}
  Log To Console       Num value is ${response}

Scenario: As a visitor I can visit the django logout page
  Go To  ${SERVER}
  Create Session   azure   http://localhost:8765/energy/api/Logout
  ${response}=   GET Request    azure    /token
  Check Response Status   ${response}
  Log To Console       Num value is ${response}

Scenario: As a visitor I can visit the django fb page
  Go To     https://www.facebook.com

  [Teardown]    Close Browser
