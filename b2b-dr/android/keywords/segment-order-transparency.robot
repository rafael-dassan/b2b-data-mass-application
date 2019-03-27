*** Settings ***

Resource      ${CURDIR}/libraries.robot
#Resource     ${CURDIR}/../variables/variables-global.robot
#Resource     ${CURDIR}/../keywords/common.robot

#Variables    ${CURDIR}/../variables/debug-drawer.py
#Variables    ${CURDIR}/../variables/authentication-flow.py

*** Keywords ***

I am authenticated
    std.Log    Implements-me.

I go to My Account screen
    std.Log    Implements-me.

I am on My Account screen
    std.Log    Implements-me.

I click on "orders" tab
    std.Log    Implements-me.

I validate the sent segment event on analytics console
    std.Log    Implements-me.