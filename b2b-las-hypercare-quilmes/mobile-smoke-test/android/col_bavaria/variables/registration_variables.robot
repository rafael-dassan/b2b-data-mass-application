*** Variables ***

# Screen elements
${ET_FIRST_NAME}                      id=firstName
${ET_LAST_NAME}                       id=lastName
${ET_EMAIL_ADDRESS}                   id=emailAddress
${ET_EMAIL_ADDRESS_CONFIRM}           id=emailConfirmationAddress
${ET_PHONE_NUMBER}                    id=phoneNumber
${BTN_NEXT_REGISTRATION_STEP}         id=nextButton
${ET_CUSTOMER_ID}                     id=customerId
${ET_LEGAL_ID}                        id=legalIdNumber
${TV_EMAIL_FORMAT_ERROR}              id=emailLoginError
${TV_EMAIL_MATCH_ERROR}               id=emailConfirmationLoginError
${TV_ABOUT_TO_BE_CREATED}             id=aboutToBeCreatedText
${TV_MESSAGE_TEXT}                    id=message
${TV_MESSAGE_EMAIL}                   id=email
${BTN_SOUNDS_GOOD}                    id=soundsGoodBtn
${LBL_INCORRET_EMAIL}                 id=emailInCorrectLabel
${TV_UPDATE_EMAIL}                    id=updateEmailAddressLink
${IV_QUILMES_FLAG}                    id=flag
${TV_REGISTRATION_MESSAGE}            id=android:id/message
${TP_REGISTRATION_MESSAGE}            id=android:id/topPanel
${BTN_REGISTRATION_CONFIRM}           id=android:id/button2

# Credentials
${NEW_USER_FIRST_NAME}                UserTest
${NEW_USER_LAST_NAME}                 AB InBev    
${NEW_USER_PHONE}                     12345678
${NEW_USER_CUSTOMERID}                386041
${NEW_USER_LEGALID}                   20303222562
${EMAIL_WRONG_FORMAT}                 test-ab-inbev
${EMAIL_DO_NOT_MATCH}                 test-test@ab-inbev.com
${USED_EMAIL}                         386041@mailinator.com
${INVALID_CUSTOMERID}                 123456
${INVALID_LEGALID}                    12345678900

# Messages
${EMAIL_FORMAT_ERROR_MESSAGE}         El usuario ingresado no es válido. Por favor verificá tus datos para continuar.
${EMAIL_MATCH_ERROR_MESSAGE}          Los correos electrónicos no coinciden. Por favor verificarlos.
${USER_NOT_FOUND_ERROR_MESSAGE}       Falló: ¡Cliente no encontrado! Verifica tus datos
${REGISTRATION_DIALOG_BTN_MESSAGE}    CONFIRMAR
${SUCCESSFULLY_REGISTRATION_MESSAGE}  Tu cuenta fue creada con éxito!
${USED_EMAIL_MESSAGE}                 Falló: Esta cuenta ya ha sido asociada