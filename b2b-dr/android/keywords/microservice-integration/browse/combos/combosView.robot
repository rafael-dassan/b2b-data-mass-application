*** Settings ***
Library             Collections
Resource            ../../../../variables/browse.robot


*** Variables ***
${combo.title} =                        title
${combo.description} =                  description
${combo.prices} =                       prices
${combo.discountedPrice} =              discounted


*** Keywords ***
I click the menu item combos
    Page Should Contain Element         ${homeMenu}
    appium.Click Element                ${homeMenu}
    Wait Until Page Contains Element    ${drawerMenu}
    Page Should Contain Element         ${combosMenu}
    Click Element                       ${combosMenu}


I check if the page was shown
    Page Should Contain Element         ${combosTable}


I get all the mobile combos and save on a list
    BuiltIn.Log To Console              I get all the mobile combos and save on a list
    ${combosList} =                     BuiltIn.Create List

    :FOR    ${index}    IN RANGE    99999
        \   ${combos} =                 I read the combos in the screen
        \   ${combosList} =             Combine Lists    ${combosList}   ${combos}
        \   ${comboText1} =             Run Keyword   Get Combo Title  ${index}
        \   Swipe by percent            30    90    30    50    duration=2000
        \   BuiltIn.Sleep               2s
        \   ${comboText2} =             Run Keyword   Get Combo Title  ${index}
        \   BuiltIn.Exit For Loop If    '${comboText1}'=='${comboText2}'

    ${combosList} =                     Remove Duplicates   ${combosList}

    [Return]                            ${combosList}


I read the combos in the screen
    BuiltIn.Log To Console              I read the combos in the screen
    ${combosList} =                     BuiltIn.Create List

    :FOR    ${index}    IN RANGE    99999
        \   ${combo1} =                 Run Keyword   Get Combo From View  ${index}
        \   ${comboText1} =             Run Keyword   Get Combo Title  ${index}
        \   Append To List              ${combosList}   ${combo1}
        \   BuiltIn.Exit For Loop If    '${comboText1}'=='${noCombo}'

    [Return]                            ${combosList}


Get Combo From View
    [Arguments]                         ${index}
    std.Log To Console                  Get Combo Text From View

    ${comboDictionary} =                BuiltIn.Create Dictionary

    ${textTitle} =                      Run Keyword    Get Combo Title  ${index}
    ${textDescription} =                Run Keyword    Get Combo Description  ${index}
    ${textDiscountedPrice} =            Run Keyword    Get Combo Discounted Price  ${index}

    ${hasTitle} =                       BuiltIn.Evaluate    '${textTitle}'!='${noCombo}'
    Run Keyword If                      ${hasTitle}==True   Set To Dictionary   ${comboDictionary}  ${combo.title}   ${textTitle}
    Run Keyword If                      ${hasTitle}==True   Set To Dictionary   ${comboDictionary}  ${combo.description}   ${textDescription}
    Run Keyword If                      ${hasTitle}==True   Set To Dictionary   ${comboDictionary}  ${combo.discountedPrice}   ${textDiscountedPrice}

    [Return]                            ${comboDictionary}


Get Combo Title
    [Arguments]                         ${index}
    ${i} =                              BuiltIn.Evaluate    ${index} + ${1}
    ${xpath} =                          BuiltIn.Catenate    ${comboTitlePrefix}${leftBrackets}${i}${rightBrackets}${slash}${comboTitleSufix}
    ${title} =                          Get Text From Xpath     ${xpath}

    [Return]                            ${title}


Get Combo Description
    [Arguments]                         ${index}
    ${i} =                              BuiltIn.Evaluate    ${index} + ${1}
    ${xpath} =                          BuiltIn.Catenate    ${comboDescriptionPrefix}${leftBrackets}${i}${rightBrackets}${slash}${comboDescriptionSufix}
    ${desc} =                           Get Text From Xpath     ${xpath}

    [Return]                            ${desc}


Get Combo Discounted Price
    [Arguments]                         ${index}
    ${i} =                              BuiltIn.Evaluate    ${index} + ${1}
    ${xpath} =                          BuiltIn.Catenate    ${comboDiscountedPricePrefix}${leftBrackets}${i}${rightBrackets}${slash}${comboDiscountedPriceSufix}
    ${desc} =                           Get Text From Xpath     ${xpath}

    [Return]                            ${desc}


Get Text From Xpath
    [Arguments]                         ${xpath}
    ${exist} =                          Run Keyword And Return Status   Page Should Contain Element     ${xpath}
    ${text} =                           Run Keyword If  ${exist}==True      Get Text    ${xpath}    ELSE    BuiltIn.Set Variable    ${noCombo}

    [Return]                            ${text}


Assert Combo Title
    [Arguments]                         ${comboAPI}     ${comboMobile}
    ${titleAPI} =                       Get From Dictionary     ${comboAPI}     ${combo.title}
    ${descAPI} =                        Get From Dictionary     ${comboAPI}     ${combo.description}

    ${titleLength} =                    BuiltIn.Get Length  ${titleAPI}
    ${titleExist} =                     Run Keyword And Return Status   BuiltIn.Should Not Be Equal     ${titleLength}   ${0}
    ${titleAPI}=                        BuiltIn.Set Variable If     ${titleExist}==False    ${descAPI}   ${titleAPI}

    ${titleMobile} =                    Get From Dictionary     ${comboMobile}     ${combo.title}

    ${message} =                        BuiltIn.Catenate  "Expected value for title was "  ${titleAPI}  " and found "  ${titleMobile}  "
    BuiltIn.Should Be Equal As Strings  ${titleAPI}  ${titleAPI}  ${message}
    BuiltIn.Log To Console              ${message}


Assert Combo Description
    [Arguments]                         ${comboAPI}     ${comboMobile}
    ${titleAPI} =                       Get From Dictionary     ${comboAPI}     ${combo.title}
    ${descAPI} =                        Get From Dictionary     ${comboAPI}     ${combo.description}

    ${titleLength} =                    BuiltIn.Get Length  ${titleAPI}
    ${titleExist} =                     Run Keyword And Return Status   BuiltIn.Should Not Be Equal     ${titleLength}   ${0}
    ${descAPI} =                        BuiltIn.Set Variable If     ${titleExist}==False    ${noCombo}  ${descAPI}

    ${descMobile} =                     Get From Dictionary     ${comboMobile}     ${combo.description}

    ${message} =                        BuiltIn.Catenate  "Expected value for description was "  ${descAPI}  " and found "  ${descMobile}  "
    BuiltIn.Should Be Equal As Strings  ${descMobile}  ${descAPI}  ${message}
    BuiltIn.Log To Console              ${message}


Assert Combo Discounted Price
    [Arguments]                         ${comboAPI}     ${comboMobile}
    ${pricesAPI} =                      Get From Dictionary     ${comboAPI}     ${combo.prices}
    ${discountedAPINumber} =            Get From Dictionary     ${pricesAPI}     ${combo.discountedPrice}
    ${discountedAPI} =                  Evaluate    "%.2f" % ${discountedAPINumber}

    ${discountedMobile} =               Get From Dictionary     ${comboMobile}     ${combo.discountedPrice}

    ${regex} =                          BuiltIn.Set Variable    [^0-9\s]
    ${regexMobile} =                    Replace String Using Regexp     ${discountedMobile}   ${regex}   ${noCombo}
    ${regexAPI} =                       Replace String Using Regexp     ${discountedAPI}   ${regex}   ${noCombo}

    ${message} =                        BuiltIn.Catenate  "Expected value for discounted price was "  ${regexAPI}  " and found "  ${regexMobile}  "
    BuiltIn.Should Be Equal As Strings  ${regexMobile}  ${regexAPI}     ${message}
    BuiltIn.Log To Console              ${message}