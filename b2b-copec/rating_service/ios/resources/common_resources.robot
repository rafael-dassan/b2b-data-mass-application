*** Settings ***
Library     AppiumLibrary
Resource    ./variables.robot


*** Keywords ***


I opened the Application
    [Arguments]     ${app}      ${bundle}
    Open Application    http://localhost:4723/wd/hub    platformName=iOS    platformVersion=12.1   deviceName=iPhone 7     app=${app}     bundIeId=${bundle}
    Wait Until Page Contains Element        accessibility_id=Allow          
    Click Element       accessibility_id=Allow 
    #Wait Until Page Contains Element        //XCUIElementTypeImage[@name="launchImageMedium"]       timeout=10
    #uncomment the next row when Mi Tienda scenarios are running
    Wait Until Page Contains Element        accessibility_id=onboardingBg.png


I set environment
    [Arguments]     ${env}
    #Tap     //XCUIElementTypeImage[@name="launchImageMedium"]     x_offset=50       y_offset=50       count=3
    #uncomment the next row when Mi Tienda scenarios are running
    Tap     accessibility_id=onboardingBg.png     x_offset=50       y_offset=50       count=3
    Wait Until Element Is Visible       ${env}     50 
    Click Element       ${env}
    Wait Until Page Contains Element     //XCUIElementTypeNavigationBar[@name="Debug Drawer"]
    Swipe       106    456    353    456
        

Click on login button
    Click Element                       //XCUIElementTypeButton[@name="Login btn"]
    Wait Until Page Contains Element    //XCUIElementTypeTextField[@name="Email Address Login"]


I enter my credentials
    [Arguments]                         ${email}    ${password}
    Input Text                          //XCUIElementTypeTextField[@name="Email Address Login"]     ${email}
    Input Password                      //XCUIElementTypeSecureTextField[@name="Password"]          ${password}


I click on Login
    Click Element                       //XCUIElementTypeButton[@name="Login"]                      timeout=20
    # Wait Until Page Contains Element    accessibility_id= Bodega Maria

I select the POC 
    [Arguments]         ${poc}
    Click Element       accessibility_id=${poc}



# AQUI DEVERA APARECER A MODAL DO RATING SERVICE


the rating service screen is displayed
   Wait Until Page Contains Element     id=ratingIncludeToolbar

I select one star
    Click Element At Coordinates    267    538
            
   
I select one tag
    [Arguments]     ${tag}
    Click Text      ${tag}
    Wait Until Page Contains Element     id=ratingSubmitButton

I click on submit
    Click Element                        id=ratingSubmitButton      
    Wait Until Page Contains Element     id=sentCloseButton

the thank you screen should be displayed
    Wait Until Page Contains Element     id=sentCloseButton
    Click Element        id=sentCloseButton

I'm redirected to home screen
    Wait Until Page Contains Element        //XCUIElementTypeNavigationBar[@name="¡Novedad!"]
    Click Element       //XCUIElementTypeNavigationBar[@name="¡Novedad!"]/XCUIElementTypeButton  


the rating service modal shouldnt be displayed
    Wait Until Page Does Not Contain        id=ratingIncludeToolbar   #verificar nome correto



    
# I go to home screen
#     Wait Until Page Contains Element        //XCUIElementTypeSearchField[@name="Search All"]

# I open My Account
#     Click Element       //XCUIElementTypeButton[@name="My Account"]
#     Sleep       5
#     Wait Until Page Contains Element        //XCUIElementTypeStaticText[@name="My Account"]

# I log out the Application
#     Click Element       //XCUIElementTypeButton[@name="Settings btn"]
#     Wait Until Page Contains Element        //XCUIElementTypeButton[@name="Log Out"]
#     Click Element       //XCUIElementTypeButton[@name="Log Out"]   





# I am logged
#     I opened the Application   
#     I set QA environment
#     Login on Application 


# the rating service screen is displayed
#     Verify if is the rating screen


# I select five stars
#     Tap on last stars

# I click on submit
#     Tap on button

# the thank you screen should be displayed
#     Verify if is the thanks screen

   
# I filled the comment area
#     Input some text 


# I select one star
#     Tap on firt star

# I select one tag
#     Verify if the tags are displayed
#     Select one tag

      
# I select three tags
#     Verify if the tags are displayed
#     Select three tag


# the submit button should appear disable
#     Verify

# Log out the Application
#     I click on my account button
#     I click on settings button
#     I click on log out button







