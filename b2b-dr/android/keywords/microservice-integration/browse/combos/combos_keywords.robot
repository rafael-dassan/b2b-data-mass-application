*** Settings ***
Library             Collections
Resource            ../../../../../microservice/CombosMicroservice.robot
Resource            ../../../../keywords/microservice-integration/browse/combos/combosView.robot
Resource            combosView.robot


*** Keywords ***

I select the combos menu
    BuiltIn.Log To Console	            \nI select the combos menu
    Run Keyword                         I click the menu item combos


I verify the combos were successfully loaded
    BuiltIn.Log To Console	            \nI verify the combos were successfully loaded
    BuiltIn.Sleep                       5s
    Run Keyword                         I check if the page was shown


I get the information from the microservice
    BuiltIn.Log To Console              I get the information from the microservice
    Run Keyword                         I get combos from api
    ${combosListMobile} =               I get all the mobile combos and save on a list
    Set Test Variable                   ${combosListMobile}

    BuiltIn.Log To Console              Combos From API: ${combos_json}
    BuiltIn.Log To Console              Combos From Mobile: ${combosListMobile}


I compare the information shown with the information from the microservice
    BuiltIn.Log To Console              I compare the information shown with the information from the microservice

    ${count} =                          BuiltIn.Get Length  ${combos_json}

    :FOR    ${i}    IN RANGE            ${count}
        \  ${comboAPI} =                BuiltIn.Set Variable    ${combos_json[${i}]}
        \  ${comboMob} =                BuiltIn.Set Variable    ${combosListMobile[${i}]}
        \  Assert Combo Title           ${comboAPI}     ${comboMob}
        \  Assert Combo Description     ${comboAPI}     ${comboMob}
        \  Assert Combo Discounted Price  ${comboAPI}     ${comboMob}