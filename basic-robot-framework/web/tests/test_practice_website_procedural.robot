*** Settings ***
Resource          ../resource/resource_web.robot
Test Setup        Open Browser  about:blank  headlesschrome
Test Teardown     Close Browser

*** Test Cases ***
Test Case 01: Search For Existent Product
  Access the home page
  Type the product "Blouse" in the search field
  Click on the search button
  Check if the product "Blouse" was listed

Test Case 02: Search For Non-Existent Product
  Access the home page
  Type the product "itemNãoExistente" in the search field
  Click on the search button
  Check the error message "No results were found for your search "itemNãoExistente""