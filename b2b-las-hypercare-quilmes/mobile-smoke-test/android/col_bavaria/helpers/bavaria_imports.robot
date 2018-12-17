*** Settings ***

Resource    ${CURDIR}/../../global_imports.robot
Resource    ${CURDIR}/../../global_variables.robot

# Keywords
Resource    ${CURDIR}/../../keywords/common_keywords.robot
Resource    ${CURDIR}/../../keywords/registration_keywords.robot
Resource    ${CURDIR}/../../keywords/manage_account_keywords.robot
Resource    ${CURDIR}/../../keywords/post_order_keywords.robot
Resource    ${CURDIR}/../keywords/bavaria_login_keywords.robot

# Variables
Resource    ${CURDIR}/../variables/bavaria_variables.robot
Resource    ${CURDIR}/../variables/login_variables.robot
Resource    ${CURDIR}/../variables/registration_variables.robot
Resource    ${CURDIR}/../variables/manage_account_variables.robot
Resource    ${CURDIR}/../variables/post_order_variables.robot