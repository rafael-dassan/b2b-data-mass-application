*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${URL}      http://automationpractice.com
${BROWSER}  headlesschrome
${PRODUTO}  Blouse

*** Keywords ***
# Step-by-step
Acessar a página home do site
    # ${options}=   Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
    # Call Method   ${options}   add_argument   --no-sandbox
    # Call Method   ${options}   add_argument   --disable-setuid-sandbox 
    # Create WebDriver   ${BROWSER}   chrome_options=${options}
    Go To   ${URL}
    Title Should Be  My Store

Digitar o nome do produto "${PRODUTO}" no campo de pesquisa
    Input Text  id=search_query_top  ${PRODUTO}

Clicar no botão pesquisar
    Click Element  name=submit_search

Conferir se o produto "${PRODUTO}" foi listado no site
    Wait Until Element Is Visible  css=#center_column > h1
    Title Should Be                Search - My Store
    Page Should Contain Image      xpath=//*[@id="center_column"]//*[@src="${URL}/img/p/7/7-home_default.jpg"]
    Page Should Contain Link       xpath=//*[@id="center_column"]//a[@class="product-name"][contains(text(),"${PRODUTO}")]

Conferir mensagem de erro "${MENSAGEM_ALERTA}"
    Wait Until Element Is Visible  //*[@id="center_column"]/p[@class="alert alert-warning"]
    Element Text Should Be         //*[@id="center_column"]/p[@class="alert alert-warning"]  ${MENSAGEM_ALERTA}