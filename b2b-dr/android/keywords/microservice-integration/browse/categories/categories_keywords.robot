*** Settings ***
Library             Collections
Resource            ../../../../variables/browse.robot
Resource            ../../../../../common_keywords/json_keywords.robot
Resource            ../../../../../microservice/variables.robot
Resource            ../../../../../microservice/CategoriesMicroservice.robot
Resource            categoryView.robot


*** Keywords ***

I Verify the screen is successfully loaded
    BuiltIn.Log To Console	            \nI Verify the screen is successfully loaded
    BuiltIn.Sleep                       5s

    Run Keyword                         I Verify if Rating Service is shown
    Run Keyword                         I Verify Try Again button
    Run Keyword                         I Verify if Categories view is shown


I Verify if Rating Service is shown
    BuiltIn.Log To Console              I Verify if Rating Service is shown
    :FOR      ${i}      IN RANGE        5
            \   BuiltIn.Log To Console   Try #${i}
            \   ${ratingShown} =        Run Keyword And Return Status    Wait Until Page Contains Element    ${ratingServiceCloseButton}     timeout=${timeout}  error=False
            \   BuiltIn.Log To Console   Rating Shown: ${ratingShown}
            \   Run Keyword If          ${ratingShown}==True    I click the Rating Service close button
        \   BuiltIn.Exit For Loop If    ${ratingShown}==False


I click the Rating Service close button
    BuiltIn.Log To Console              I click the Rating Service close button
    Click Element                       ${ratingServiceCloseButton}


I Verify Try Again button
    BuiltIn.Log To Console              I Verify Try Again button
    :FOR      ${i}      IN RANGE        5
            \   BuiltIn.Log To Console   Try #${i}
            \   ${tryAgainShown} =      Run Keyword And Return Status    Wait Until Page Contains Element    ${tryAgain}     timeout=${timeout}  error=False
            \   BuiltIn.Log To Console   Is Try Again Shown: ${tryAgainShown}
            \   Run Keyword If          ${tryAgainShown}==True    I click the Try Again button
        \   BuiltIn.Exit For Loop If    ${tryAgainShown}==False


I click the Try Again button
    BuiltIn.Log To Console              I click the Try Again button
    Click Element                       ${tryAgain}


I select the first category
    I select the category               ${2}


I select the first sub-category
    I select the sub-category           ${1}


I Verify items were successfully loaded
    BuiltIn.Log To Console              I Verify items were successfully loaded
    BuiltIn.Sleep                       5s
    Wait Until Page Contains Element    ${categoryView}     timeout=${timeout}  error=False
    BuiltIn.Log To Console              I Verify category's image is displayed
    Page Should Contain Element         ${categoryImage}
    BuiltIn.Log To Console              I Verify category's items are displayed
    Page Should Contain Element         ${categoryItemsCard1}


I compare with the categories shown
    BuiltIn.Log To Console              I compare with the categories shown

    ${categoriesList} =                 I get all the mobile categories and save on a list
    ${count} =                          BuiltIn.Get Length  ${json}

    :FOR    ${i}      IN RANGE          ${count}
        \   ${index} =                  Builtin.Evaluate    ${i} + ${2}
        \   ${text} =                   Get From List   ${categoriesList}   ${i}
        \   ${textCount} =              BuiltIn.Get Length  ${text}
        \   Run Keyword If              ${textCount}>${0}   BuiltIn.Log To Console   Category: ${text}
        \   Json Property Should Equal  ${json[${i}]}     name     ${text}
        \   ${imageView} =              Get Category Image View    ${i}
        \   Page Should Contain Element   ${imageView}
        \   Run Keyword                 I select the category  ${i}
        \   I compare with the sub-categories shown  ${i}


I compare with the sub-categories shown
    [Arguments]                         ${index}
    BuiltIn.Log To Console              I compare with the sub-categories shown

    Run Keyword                         I Verify the sub-categories were successfully loaded
    ${subCategoriesService} =           I get sub-categories from index     ${index}
    ${subCategoriesMobile} =            I get the mobile sub-categories and save on a list

    ${count} =                          BuiltIn.Get Length  ${subCategoriesService}

    :FOR    ${i}    IN RANGE            ${count}
        \   ${text} =                   Get From List   ${subCategoriesMobile}   ${i}
        \   ${textCount} =              BuiltIn.Get Length  ${text}
        \   Run Keyword If              ${textCount}>${0}   BuiltIn.Log To Console   Sub-Category: ${text}
        \   ${subCategoryitem} =        Get json at index  ${subCategoriesService}   ${i}
        \   Run Keyword                 Json Property Should Equal  ${subCategoryitem}     name     ${text}
        \   ${imageView} =              Get Sub-Category Image View     ${i}
        \   Page Should Contain Element   ${imageView}
        \   Run Keyword                 I select the sub-category   ${i}
        \   Run Keyword                 I compare the amount of items shown  ${subCategoryitem}

    Run Keyword                         Close sub-category screen


I compare the amount of items shown
    [Arguments]                         ${subCategory}
    BuiltIn.Log To Console              I compare the amount of items shown

    ${itemsService} =                   I get the items from sub-category  ${subCategory}
    ${countService} =                   BuiltIn.Get Length  ${itemsService}
    BuiltIn.Log To Console              Item Count - Service: ${countService}

    ${itemsMobile} =                    I get the mobile items and save on a list
    ${countMobile} =                    BuiltIn.Get Length  ${itemsMobile}
    BuiltIn.Log To Console              Item Count - Mobile: ${countMobile}

    BuiltIn.Should Be Equal             ${countService}   ${countMobile}
    BuiltIn.Log To Console              Item Count Service: ${countService} is equals to Item Count Mobile: ${countMobile}
    Run Keyword                         Close items screen