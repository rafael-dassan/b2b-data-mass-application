*** Settings ***
Resource          ../resource/resource_web.robot
Test Setup        Open Browser  about:blank  headlesschrome
Test Teardown     Close Browser

*** Test Cases ***
Test Case 01: Pesquisar produto existente
  Acessar a página home do site
  Digitar o nome do produto "Blouse" no campo de pesquisa
  Clicar no botão pesquisar
  Conferir se o produto "Blouse" foi listado no site

Test Case 02: Pesquisar produto não existente
  Acessar a página home do site
  Digitar o nome do produto "itemNãoExistente" no campo de pesquisa
  Clicar no botão pesquisar
  Conferir mensagem de erro "No results were found for your search "itemNãoExistente""