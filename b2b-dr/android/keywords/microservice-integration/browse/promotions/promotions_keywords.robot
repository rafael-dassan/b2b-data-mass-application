*** Settings ***
Resource            ../../../../variables/browse.robot


*** Keywords ***
I check there are banners
    BuiltIn.Log To Console          I check there are banners
    BuiltIn.Sleep                   5s
    Page Should Contain Element     ${promotionView}


I am able to swipe over the banner
    BuiltIn.Log To Console          I am able to swipe over the banner
    Page Should Contain Element     ${promotion1}
    Page Should Contain Element     ${promotion2}
    Swipe By Percent                20  20  95  20  duration=500