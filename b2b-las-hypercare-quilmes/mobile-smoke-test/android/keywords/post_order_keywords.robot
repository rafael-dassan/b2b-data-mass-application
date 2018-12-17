*** Keywords ***

I add products to My Truck
    [Arguments]                                         ${product_type}  ${quantity}
    appium.Text Should Be Visible                       ${product_type}
    appium.Click Text                                   ${product_type}        
    appium.Wait Until Page Contains Element             ${TV_SPECIFIC_BEER}  ${TIMEOUT}
    appium.Click Element                                ${TV_SPECIFIC_BEER}
    appium.Wait Until Page Contains Element             ${IV_BRAND_IMAGE}  ${TIMEOUT}
    appium.Input Text                                   ${ET_ADD_PRODUCT_QUANTITY}  ${quantity}
    appium.Press Keycode                                66  # Pressing ENTER key
    std.Sleep                                           200ms
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/adding_products_to_my_truck.png
    I go to My Truck

I go to My Truck
    appium.Click Element                                ${IV_TRUCK}
    appium.Page Should Contain Text                     ${MY_TRUCK}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/my_truck_screen.png

I post the order
    ${attribute_value}                                  appium.Get Element Attribute  ${BTN_SUBMIT_ORDER}  enabled
    std.Log                                             \nButton attribute: ${attribute_value}  console=yes 
    std.Run Keyword If                                  '${attribute_value}' != 'true' 
    ...                                                 appium.Wait Until Page Does Not Contain Element  
    ...                                                 ${TV_LOADING_TITLE}  ${TIMEOUT}
    appium.Input Text                                   ${TV_ORDER_NUMBER}  ${ORDER_NUMBER}
    # Get Order Total
    appium.Swipe By Percent                             50  80  50  30  350  
    appium.Wait Until Element Is Visible                ${TV_TOTAL_ORDER}      
    ${order_total_price}                                appium.Get Text  ${TV_TOTAL_ORDER}
    std.Set Global Variable                             ${ORDER_TOTAL}  ${order_total_price}
    std.Log                                             \nOrder total: ${ORDER_TOTAL}  console=yes
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/order_to_be_posted.png
    # Validate Order Minimum
    ${order_minimum_message}                            appium.Get Text  ${TV_MINIMUM_ORDER}
    std.Run Keyword If                                  '${order_minimum_message}' == '${MINIMUM_ORDER_COMPLETED_MESSAGE}'    
    ...                                                 appium.Click Element  ${BTN_SUBMIT_ORDER}   

The order must be processed successfully
    appium.Wait Until Page Contains Element             ${BTN_SUBMIT_ORDER}  ${TIMEOUT}
    appium.Element Should Be Enabled                    ${BTN_SUBMIT_ORDER}
    appium.Click Element                                ${BTN_SUBMIT_ORDER}
    appium.Wait Until Page Contains Element             ${TV_ORDER_PLACED}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_STATUS_ORDER}  ${ORDER_STATUS_MESSAGE}    
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/order_posted_successfully.png
    Check Recent Orders
    # Delivery window available
    # appium.Wait Until Page Contains Element             ${LAYOUT_DELIVERY_WINDOW}
    # If no delivery window
    # ${delivery_window_message}                          appium.Get Text  ${TV_NO_DELIVERY_WINDOW}
    # std.Run Keyword If                                  '${delivery_window_message}' == '${NO_DELIVERY_WINDOW_MESSAGE}'
    # ...                                                 appium.Click Element  ${BTN_SUBMIT_ORDER}
    
I remove all the products
    appium.Wait Until Page Contains Element             ${ET_ADD_REMOVE_PRODUCT_TRUCK}  ${TIMEOUT}
    ${attribute_value}                                  appium.Get Element Attribute  ${BTN_SUBMIT_ORDER}  enabled
    std.Log                                             \nButton attribute: ${attribute_value}  console=yes 
    std.Run Keyword If                                  '${attribute_value}' != 'true' 
    ...                                                 appium.Wait Until Page Does Not Contain Element     
    ...                                                 ${TV_LOADING_TITLE}  ${TIMEOUT}
    appium.Swipe By Percent                             05  30	95  30  350       

The truck must be empty
    appium.Wait Until Page Contains Element             ${TV_TRUCK_EMPTY}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_TRUCK_EMPTY}  ${TRUCK_EMPTY_MESSAGE}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/empty_truck.png

Check Recent Orders
    appium.Click Element                                ${TV_RECENT_ORDERS_LINK}
    appium.Wait Until Page Does Not Contain Element     ${TV_LOADING_TITLE}  ${TIMEOUT}
    appium.Page Should Contain Element                  ${ORDERS_TAB}  ${TIMEOUT}
    ${latest_order_status}                              appium.Get Text  ${TV_STATUS_SENT}
    std.Log                                             ${latest_order_status}      console=true
    std.Should Contain Any                              ${latest_order_status}  @{order_statuses} 
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/empty_truck.png

I must not be able to post the order
    appium.Wait Until Page Contains Element             ${TV_MINIMUM_ORDER}  ${TIMEOUT}
    ${order_minimum_message}                            appium.Get Text  ${TV_MINIMUM_ORDER}
    std.Log                                             \nOrder minimum: ${order_minimum_message}  console=yes
    std.Should Be True                                  '${order_minimum_message}' != '${MINIMUM_ORDER_COMPLETED_MESSAGE}'
    appium.Element Should Be Disabled                   ${BTN_SUBMIT_ORDER}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/post_order/minimum_order_not_completed.png