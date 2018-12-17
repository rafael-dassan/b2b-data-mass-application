*** Variables ***

# Screen elements
# Menu
${TV_CUSTOMER_ID}                id=customer_id
${CHANGE_ACCOUNT_DROPDOWN}       id=drawer_arrow

# Settings screen
${LBL_MY_ACCOUNT}                           id=myAccountLbl              
${CHANGE_PASSWORD_CELL}                     id=changePasswordCell
${CONNECT_NEW_ACCOUNT_CELL}                 id=connectNewAccountCell

# Change password screen
${ET_CURRENT_PASSWORD}                      id=secureCode
${ET_NEW_PASSWORD}                          id=newPassword
${ET_CONFIRM_NEW_PASSWORD}                  id=confirmNewPassword
${TV_MESSAGE_PASSWORD}                      id=invalidPassword
${BTN_PASSWORD_CHANGE}                      id=nextButton
${TP_PASSWORD_CHANGE_DIALOG}                android:id/topPanel
${TV_PASSWORD_CHANGE}                       id=android:id/message
${BTN_PASSWORD_CHANGE_DIALOG}               id=android:id/button2

# Credentials
# Change password credentials
${NEW_PASSWORD}                             Las12345
${NEW_PASSWORD_NOT_MATCH}                   Las12345!
${PASSWORD_MINIMUM_LENGTH}                  LasLas
${PASSWORD_INVALID_FORMAT}                  las12345                  

# Switch account credentials
${POC_SWITCH_ACCOUNT}                       PATIÑO FLAVIA PAMELA | 378890
${POC_NUMBER_SWITCH_ACCOUNT}                378890

# Messages
${PASSWORD_CHANGE_SUCESSFULL_MESSAGE}       Su contraseña ha sido actualizada.
${PASSWORD_CHANGE_INVALID_MESSAGE}          Fail: Incluir mínimo 3 caracteres diferentes en la contraseña. Los tipos de caracteres son: minúsculas, mayúsculas, dígitos, caracteres especiales.
${PASSWORD_CHANGE_MINIMUM_LENGTH_MESSAGE}   La longitud mínima debe ser de 8 caracteres con la combinación de un símbolo, una mayúscula y un número.
${PASSWORD_NOT_MATCHING_MESSAGE}            Las contraseñas que has ingresado son distintas
${INVALID_CURRENT_PASSWORD_MESSAGE}         Su contraseña es incorrecta. Por favor introducir de nuevo.
${PASSWORD_CHANGE_CONFIRM_DIALOG_MESSAGE}   CONFIRMAR
${MENU_SETTINGS_MESSAGE}                    Configurar