*** Settings ***
Documentation   Documentação da API: https://fakerestapi.azurewebsites.net/swagger/ui/index#!/Books
Library         RequestsLibrary
Library         Collections

*** Variable ***
${URL_API}                              https://fakerestapi.azurewebsites.net/api/
${POST_RESPONSE_HEADER_CONTENT_TYPE}    application/json; charset=utf-8
${POST_RESPONSE_HEADER_CONTENT_LENGTH}  241
${POST_RESPONSE_HEADER_VARY}            Accept-Encoding
&{BOOK_15}                              ID=15
...                                     Title=Book 15
...                                     PageCount=1500
&{BOOK_201}                             ID=201
...                                     Title=Book 201
...                                     Description=This is the Book 201
...                                     PageCount=300
...                                     Excerpt=This is the excerpt of the Book 201
...                                     PublishDate=2018-11-13T12:38:52.983Z


*** Keywords ***
# Setup
Conectar a minha API
    Create Session      fakeAPI  ${URL_API}  disable_warnings=1
    ${HEADERS}          Create Dictionary  content-type=application/json
    Set Suite Variable  ${HEADERS}

# Passo-a-passo
Requisitar todos os livros
    ${RESPOSTA}        Get Request  fakeAPI  Books
    Log                ${RESPOSTA.text}
    Set Test Variable  ${RESPOSTA}

Requisitar o livro "${ID_LIVRO}"
    ${RESPOSTA}        Get Request  fakeAPI  Books/${ID_LIVRO}
    Log                ${RESPOSTA.text}
    Set Test Variable  ${RESPOSTA}

Cadastrar um novo livro
    ${RESPOSTA}        Post Request  fakeAPI  Books
    ...                data={"ID": ${BOOK_201.ID},"Title": "${BOOK_201.Title}","Description": "${BOOK_201.Description}","PageCount": ${BOOK_201.PageCount},"Excerpt": "${BOOK_201.Excerpt}","PublishDate": "${BOOK_201.PublishDate}"}
    ...                headers=${HEADERS}
    Log                ${RESPOSTA.text}
    Set Test Variable  ${RESPOSTA}

# Conferências
Conferir o status code
    [Arguments]                 ${STATUSCODE_DESEJADO}
    Should Be Equal As Strings  ${RESPOSTA.status_code}  ${STATUSCODE_DESEJADO}

Conferir o reason
    [Arguments]                 ${REASON_DESEJADO}
    Should Be Equal As Strings  ${RESPOSTA.reason}  ${REASON_DESEJADO}

Conferir se retorna uma lista com "${QTDE_LIVROS}" livros
    Length Should Be  ${RESPOSTA.json()}  ${QTDE_LIVROS}

Conferir se retorna todos os dados corretos do livro 15
    Dictionary Should Contain Item  ${RESPOSTA.json()}  ID  ${BOOK_15.ID}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  Title  ${BOOK_15.Title}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  PageCount  ${BOOK_15.PageCount}
    Should Not Be Empty             ${RESPOSTA.json()["Description"]}
    Should Not Be Empty             ${RESPOSTA.json()["Excerpt"]}
    Should Not Be Empty             ${RESPOSTA.json()["PublishDate"]}

Conferir se retorna todos os dados cadastrados para o novo livro
    Conferir o status code  200
    Dictionary Should Contain Item  ${RESPOSTA.json()}   ID              ${BOOK_201.ID}
    Dictionary Should Contain Item  ${RESPOSTA.json()}   Title           ${BOOK_201.Title}
    Dictionary Should Contain Item  ${RESPOSTA.json()}   Description     ${BOOK_201.Description}
    Dictionary Should Contain Item  ${RESPOSTA.json()}   PageCount       ${BOOK_201.PageCount}
    Dictionary Should Contain Item  ${RESPOSTA.json()}   Excerpt         ${BOOK_201.Excerpt}
    Dictionary Should Contain Item  ${RESPOSTA.json()}   PublishDate     ${BOOK_201.PublishDate}
    Dictionary Should Contain Item  ${RESPOSTA.headers}  Content-Type    ${POST_RESPONSE_HEADER_CONTENT_TYPE}
    Dictionary Should Contain Item  ${RESPOSTA.headers}  Content-Length  ${POST_RESPONSE_HEADER_CONTENT_LENGTH}    
    Dictionary Should Contain Item  ${RESPOSTA.headers}  Vary            ${POST_RESPONSE_HEADER_VARY}