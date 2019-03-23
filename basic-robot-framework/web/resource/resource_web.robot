*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${URL}      http://automationpractice.com
${BROWSER}  headlesschrome
${PRODUCT}  Blouse

*** Keywords ***
# Step-by-step
Access the home page
    Go To   ${URL}
    Title Should Be  My Store

Type the product "${PRODUCT}" in the search field
    Input Text  id=search_query_top  ${PRODUCT}

Click on the search button
    Click Element  name=submit_search

Check if the product "${PRODUCT}" was listed
    Wait Until Element Is Visible  css=#center_column > h1
    Title Should Be                Search - My Store
    Page Should Contain Image      xpath=//*[@id="center_column"]//*[@src="${URL}/img/p/7/7-home_default.jpg"]
    Page Should Contain Link       xpath=//*[@id="center_column"]//a[@class="product-name"][contains(text(),"${PRODUCT}")]

Check the error message "${ERROR_MESAGE}"
    Wait Until Element Is Visible  //*[@id="center_column"]/p[@class="alert alert-warning"]
    Element Text Should Be         //*[@id="center_column"]/p[@class="alert alert-warning"]  ${ERROR_MESAGE}
    Capture Page Screenshot