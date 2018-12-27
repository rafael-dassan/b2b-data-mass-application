*** Settings ***
Documentation   API Documentation: https://fakerestapi.azurewebsites.net/swagger/ui/index#!/Books
Resource        ../resource/resource_api.robot
Suite Setup     Connect to the API

*** Test Cases ***
Test Case 01: GET All Books
    Perform GET request
    Check the status code    200
    Check the reason   OK
    Check if the request returns a list with "200" books

Test Case 02: GET Book By ID
    Perform GET request by ID "15"
    Check the status code    200
    Check the reason   OK
    Check if the request returns the correct data for book "15"

Test Case 03: Register a new book (POST Request)
    Perform POST request
    Check if the request returns the correct data for the new book

# TO-DO: Caso de Teste 04: Alterar um livro específico (PUT em um livro específico)
#   - Conferir se retorna todos os dados alterados do livro 150
# TO-DO: Deletar um livro (DELETE)
#   - Conferir se deleta o livro 200 (o response body deve ser vazio)\