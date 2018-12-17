*** Settings ***
Documentation	    Tests to verify that the Post Order Feature succeed and 
...               failed correctly depending on the users credentials and
...               order information.

Resource		      ${CURDIR}/../helpers/quilmes_imports.robot

Suite Setup       Bootstrap test environment
Suite Teardown	  Close App

Test Setup		    appium.Launch Application
Test Teardown	    appium.Quit Application

*** Test Cases ***

Scenario 01: Post order sucessfully
  [Tags]	high	las-automated-smoke-test  post_order
  Given I have logged into the application
    And I add products to My Truck  ${PRODUCT_TYPE}  ${PRODUCT_QUANTITY}
  When I post the order
  Then The order must be processed successfully

Scenario 02: Validate the item removal of My Truck
  [Tags]	high	las-automated-smoke-test  post_order
  Given I have logged into the application
    And I add products to My Truck  ${PRODUCT_TYPE}  ${PRODUCT_QUANTITY}
  When I remove all the products
  Then The truck must be empty

Scenario 03: Validate the non-completion of minimum order
  [Tags]	high	las-automated-smoke-test  post_order
  Given I have logged into the application
  When I add products to My Truck  ${PRODUCT_TYPE}  ${PRODUCT_MINIMUM_QUANTITY}
  Then I must not be able to post the order