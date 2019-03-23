*** Settings ***
Library         RequestsLibrary
Library         Collections

*** Variables ***
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
Connect to the API
    Create Session      fakeAPI  ${URL_API}  disable_warnings=1
    ${HEADERS}          Create Dictionary  content-type=application/json
    Set Suite Variable  ${HEADERS}

# Step-by-step
Perform GET request
    ${RESPONSE}        Get Request  fakeAPI  Books
    Log                ${RESPONSE.text}
    Set Test Variable  ${RESPONSE}

Perform GET request by ID "${ID_LIVRO}"
    ${RESPONSE}        Get Request  fakeAPI  Books/${ID_LIVRO}
    Log                ${RESPONSE.text}
    Set Test Variable  ${RESPONSE}

Perform POST request
    ${RESPONSE}        Post Request  fakeAPI  Books
    ...                data={"ID": ${BOOK_201.ID},"Title": "${BOOK_201.Title}","Description": "${BOOK_201.Description}","PageCount": ${BOOK_201.PageCount},"Excerpt": "${BOOK_201.Excerpt}","PublishDate": "${BOOK_201.PublishDate}"}
    ...                headers=${HEADERS}
    Log                ${RESPONSE.text}
    Set Test Variable  ${RESPONSE}

# Conferências
Check the status code
    [Arguments]                 ${EXPECTED_STATUS_CODE}
    Should Be Equal As Strings  ${RESPONSE.status_code}  ${EXPECTED_STATUS_CODE}

Check the reason
    [Arguments]                 ${EXPECTED_REASON}
    Should Be Equal As Strings  ${RESPONSE.reason}  ${EXPECTED_REASON}

Check if the request returns a list with "${BOOKS_QTY}" books
    Length Should Be  ${RESPONSE.json()}  ${BOOKS_QTY}

Check if the request returns the correct data for book "15"
    Dictionary Should Contain Item  ${RESPONSE.json()}  ID  ${BOOK_15.ID}
    Dictionary Should Contain Item  ${RESPONSE.json()}  Title  ${BOOK_15.Title}
    Dictionary Should Contain Item  ${RESPONSE.json()}  PageCount  ${BOOK_15.PageCount}
    Should Not Be Empty             ${RESPONSE.json()["Description"]}
    Should Not Be Empty             ${RESPONSE.json()["Excerpt"]}
    Should Not Be Empty             ${RESPONSE.json()["PublishDate"]}

Check if the request returns the correct data for the new book
    Check the status code  200
    Dictionary Should Contain Item  ${RESPONSE.json()}   ID              ${BOOK_201.ID}
    Dictionary Should Contain Item  ${RESPONSE.json()}   Title           ${BOOK_201.Title}
    Dictionary Should Contain Item  ${RESPONSE.json()}   Description     ${BOOK_201.Description}
    Dictionary Should Contain Item  ${RESPONSE.json()}   PageCount       ${BOOK_201.PageCount}
    Dictionary Should Contain Item  ${RESPONSE.json()}   Excerpt         ${BOOK_201.Excerpt}
    Dictionary Should Contain Item  ${RESPONSE.json()}   PublishDate     ${BOOK_201.PublishDate}
    Dictionary Should Contain Item  ${RESPONSE.headers}  Content-Type    ${POST_RESPONSE_HEADER_CONTENT_TYPE}
    Dictionary Should Contain Item  ${RESPONSE.headers}  Content-Length  ${POST_RESPONSE_HEADER_CONTENT_LENGTH}    
    Dictionary Should Contain Item  ${RESPONSE.headers}  Vary            ${POST_RESPONSE_HEADER_VARY}