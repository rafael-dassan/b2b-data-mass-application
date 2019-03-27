*** Settings ***
Library             Collections
Resource            ../../../../variables/browse.robot


*** Keywords ***

I Verify if Categories view is shown
    BuiltIn.Log To Console              Wait for categories view
    Wait Until Page Contains Element    ${categoriesView}
    Element Should Be Visible           ${categoriesView}


I Verify the sub-categories were successfully loaded
    BuiltIn.Log To Console              I Verify sub-categories were successfully loaded
    Wait Until Page Contains Element    ${subCategoriesView}


I select the category
    [Arguments]                         ${index}
    ${i}=                               BuiltIn.Evaluate    ${index} + ${2}
    BuiltIn.Log To Console              I select the category
    BuiltIn.Sleep                       5s
    ${xpath}=                           Get Category Title Image View  ${i}
    Click Element                       ${xpath}


Get Category Text From View
    [Arguments]                         ${index}
    ${xpath} =                          BuiltIn.Catenate    ${categoryRecyclerView}${slash}${categoryTextCardFrame}${leftBrackets}${index}${rightBrackets}${slash}${categoryTextCardSufix}
    ${viewExist} =                      Run Keyword and Return Status   Page Should Contain Element     ${xpath}
    ${text} =                           Run Keyword If  ${viewExist}==True      Get Text    ${xpath}    ELSE    BuiltIn.Set Variable    ${noCategory}
    [Return]                            ${text}


Get Category Title Image View
    [Arguments]                         ${index}
    ${xpath} =                          BuiltIn.Catenate    ${categoryRecyclerView}${slash}${categoryTextCardFrame}${leftBrackets}${index}${rightBrackets}${slash}${categoryCardImageSufix}
    [Return]                            ${xpath}


Get Category Image View
    [Arguments]                         ${index}
    ${i}=                               BuiltIn.Evaluate    ${index} + ${1}
    ${xpath} =                          BuiltIn.Catenate    ${categoryImageView}${leftBrackets}${i}${rightBrackets}
    [Return]                            ${xpath}


I select the sub-category
    [Arguments]                         ${index}
    ${i}=                               BuiltIn.Evaluate    ${index} + ${1}
    BuiltIn.Log To Console              I select the sub-category
    BuiltIn.Sleep                       5s
    ${xpath}=                           Get Sub-Category Card View  ${i}
    Click Element                       ${xpath}


Get Sub-Category Card View
    [Arguments]                         ${index}
    ${xpath} =                          BuiltIn.Catenate    ${subCategoryRecyclerView}${slash}${subCategoriesCardFrame}${leftBrackets}${index}${rightBrackets}${slash}${subcategoriescardsufix}
    [Return]                            ${xpath}


Get Sub-Category Text From View
    [Arguments]                         ${index}
    ${xpath} =                          BuiltIn.Catenate    ${subCategoryRecyclerView}${slash}${subCategoryTextCardFrame}${leftBrackets}${index}${rightBrackets}${slash}${subCategoryTextCardSufix}
    ${viewExist} =                      Run Keyword and Return Status   Page Should Contain Element     ${xpath}
    ${text} =                           Run Keyword If  ${viewExist}==True      Get Text    ${xpath}    ELSE    BuiltIn.Set Variable    ${noCategory}
    [Return]                            ${text}


Get Sub-Category Image View
    [Arguments]                         ${index}
    ${i}=                               BuiltIn.Evaluate    ${index} + ${1}
    ${xpath} =                          BuiltIn.Catenate    ${subCategoryImageView}${leftBrackets}${i}${rightBrackets}
    [Return]                            ${xpath}


Close sub-category screen
    ${buttonExist} =                    Run Keyword And Return Status   Page Should Contain Element     ${subCategoryBackButton}
    Run Keyword If                      ${buttonExist}==True  Click Element   ${subCategoryBackButton}
    BuiltIn.Sleep                       3s


Get Item Text From View
    [Arguments]                         ${index}
    ${xpath} =                          BuiltIn.Catenate    ${categoryItemsRecyclerView}${slash}${categoryItemsTextCardFrame}${leftBrackets}${index}${rightBrackets}${slash}${categoryItemsTextCardSufix}
    ${viewExist} =                      Run Keyword and Return Status   Page Should Contain Element     ${xpath}
    ${text} =                           Run Keyword If  ${viewExist}==True      Get Text    ${xpath}    ELSE    BuiltIn.Set Variable    ${noCategory}
    [Return]                            ${text}


Close items screen
    ${buttonExist} =                    Run Keyword And Return Status   Page Should Contain Element     ${categoryItemsCloseButton}
    Run Keyword If                      ${buttonExist}==True  Click Element   ${categoryItemsCloseButton}
    BuiltIn.Sleep                       3s


I get all the mobile categories and save on a list
    BuiltIn.Log To Console              I get all the mobile categories and save on a list
    ${categoriesList} =                 BuiltIn.Create list
    ${count} =                          BuiltIn.Set Variable  ${6}

    :FOR    ${index}    IN RANGE    99999
        \   Append To Categories List        ${count}  ${categoriesList}
        \   ${category1} =                   Run Keyword And Ignore Error   Get Category Text From View  ${2}
        \   Swipe by percent                 30    90    10    40
        \   BuiltIn.Sleep                    1s
        \   ${category2} =                   Run Keyword And Ignore Error   Get Category Text From View  ${2}
        \   BuiltIn.Exit For Loop If         ${category1}==${category2}

    Remove Values From List             ${categoriesList}  ${noCategory}
    ${categoriesList} =                 Remove Duplicates   ${categoriesList}
    BuiltIn.Log to console              Categories List: ${categoriesList}

    [Return]                            ${categoriesList}


Append To Categories List
    [Arguments]                         ${count}   ${categoryList}
     : FOR    ${i}    IN RANGE   2    ${count}+2
       \  ${categoryName} =             Get Category Text From View  ${i}
       \  ${textCount} =                BuiltIn.Get Length  ${categoryName}
       \  Run Keyword If                ${textCount}>${0}    BuiltIn.Log To Console   Category: ${categoryName}
       \  ${contains} =                 Run Keyword And Return Status    Collections.List Should Contain Value   ${categoryList}   ${categoryName}
       \  Run Keyword If                ${contains}==False   Append To List  ${categoryList}    ${categoryName}
       \  ${categoryNameCount} =        BuiltIn.Get Length  ${categoryName}
       \  BuiltIn.Exit For Loop If      ${categoryNameCount} == ${0}


I get the mobile sub-categories and save on a list
    BuiltIn.Log To Console              I get the mobile sub-categories and save on a list
    ${subCategoriesList} =              BuiltIn.Create list

    ${count} =                          BuiltIn.Set Variable  ${15}

    :FOR    ${index}    IN RANGE    99999
        \   Append To Sub-Categories List        ${count}  ${subCategoriesList}
        \   ${subCategory1} =                Run Keyword And Ignore Error   Get Sub-Category Text From View  ${2}
        \   Swipe by percent                 30    90    10    55
        \   BuiltIn.Sleep                    3s
        \   ${subCategory2} =                Run Keyword And Ignore Error   Get Sub-Category Text From View  ${2}
        \   BuiltIn.Exit For Loop If         ${subCategory1}==${subCategory2}

    Remove Values From List             ${subCategoriesList}  ${noCategory}
    ${subCategoriesList} =              Remove Duplicates   ${subCategoriesList}
    BuiltIn.Log To console              Sub-Categories List: ${subCategoriesList}

    [Return]                            ${subCategoriesList}


Append To Sub-Categories List
    [Arguments]                         ${count}   ${subCategoryList}
     : FOR    ${i}    IN RANGE   1    ${count}+1
       \  ${subCategoryName} =          Get Sub-Category Text From View  ${i}
       \  ${textCount} =                BuiltIn.Get Length  ${subCategoryName}
       \  Run Keyword If                ${textCount}>${0}    BuiltIn.Log To Console   Sub-Category: ${subCategoryName}
       \  ${contains} =                 Run Keyword And Return Status    Collections.List Should Contain Value   ${subCategoryList}   ${subCategoryName}
       \  Run Keyword If                ${contains}==False   Append To List  ${subCategoryList}    ${subCategoryName}
       \  ${subCategoryNameCount} =     BuiltIn.Get Length  ${subCategoryName}
       \  BuiltIn.Exit For Loop If      ${subCategoryNameCount} == ${0}


I get the mobile items and save on a list
    BuiltIn.Log To Console              I get the mobile items and save on a list
    ${itemsList} =                      BuiltIn.Create list

    ${count} =                          BuiltIn.Set Variable  ${20}

    :FOR    ${index}    IN RANGE    99999
        \   Append To Items List             ${count}  ${itemsList}
        \   ${item1} =                       Run Keyword And Ignore Error   Get Item Text From View  ${1}
        \   Swipe by percent                 30    90    10    55
        \   BuiltIn.Sleep                    3s
        \   ${item2} =                       Run Keyword And Ignore Error   Get Item Text From View  ${1}
        \   BuiltIn.Exit For Loop If         ${item1}==${item2}

    Remove Values From List             ${itemsList}  ${noCategory}
    ${itemsList} =                      Remove Duplicates   ${itemsList}
    BuiltIn.Log To console              Items List: ${itemsList}

    [Return]                            ${itemsList}


Append To Items List
    [Arguments]                         ${count}   ${itemsList}
     : FOR    ${i}    IN RANGE   1    ${count}+1
       \  ${itemName} =                 Get Item Text From View  ${i}
       \  ${textCount} =                BuiltIn.Get Length  ${itemName}
       \  Run Keyword If                ${textCount}>${0}   BuiltIn.Log To Console   Item: ${itemName}
       \  ${contains} =                 Run Keyword And Return Status    Collections.List Should Contain Value   ${itemsList}   ${itemName}
       \  Run Keyword If                ${contains}==False   Append To List  ${itemsList}    ${itemName}
       \  ${itemNameCount} =            BuiltIn.Get Length  ${itemName}
       \  BuiltIn.Exit For Loop If      ${itemNameCount} == ${0}