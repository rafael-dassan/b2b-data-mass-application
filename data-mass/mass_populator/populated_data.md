# Populated Data

## Common

### Accounts

All countries will have the Accounts created using Accounts Microservice.

Only ZA has also the two Accounts created for Microservice and Middleware (check the table below).

| Country Code | Country Name | Microservice | Middleware |
|:-----------:|:-----------:|:-----------:|:-----------:|
| AR | Argentina | Yes | No |
| BR | Brazil | Yes | No |
| CL | Chile | Yes | No |
| DO | Dominican Republic | Yes | No |
| ZA | South Africa | Yes | Yes |

#### AR

- Account 1: created with ID **5444385012**, name **AR_POC_001**, payment method **[CASH]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 2: created with ID **9932094352**, name **AR_POC_002**, payment method **[CASH]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 3: created with ID **1669325565**, name **AR_POC_003**, payment method **[CASH]**, with liquor license, without delivery window, credit **45000**, balance **45000**.

#### BR

- Account 1: created with ID **99481543000135**, name **BR_POC_001**, payment method **[CASH, BANK_SLIP]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 2: created with ID **56338831000122**, name **BR_POC_001**, payment method **[CASH, BANK_SLIP]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 3: created with ID **42282891000166**, name **BR_POC_001**, payment method **[CASH, BANK_SLIP]**, with liquor license, without delivery window, credit **45000**, balance **45000**.

#### CL

- Account 1: created with ID **2323434554**, name **CL_POC_001**, payment method **[CASH]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 2: created with ID **1020303040**, name **CL_POC_002**, payment method **[CASH]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 3: created with ID **3325534210**, name **CL_POC_003**, payment method **[CASH]**, with liquor license, without delivery window, credit **45000**, balance **45000**.

#### DO

- Account 1: created with ID **9883300001**, name **DO_POC_001**, payment method **[CASH, CREDIT]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 2: created with ID **9883300002**, name **DO_POC_002**, payment method **[CASH, CREDIT]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 3: created with ID **9883300003**, name **DO_POC_003**, payment method **[CASH, CREDIT]**, with liquor license, without delivery window, credit **45000**, balance **45000**.

#### ZA

- Account 1: created with ID **9883300101**, name **ZA_POC_001**, payment method **[CASH]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 2: created with ID **9883300102**, name **ZA_POC_002**, payment method **[CASH]**, with liquor license, with delivery window, credit **45000**, balance **45000**.
- Account 3: created with ID **9883300103**, name **ZA_POC_003**, payment method **[CASH]**, with liquor license, without delivery window, credit **45000**, balance **45000**.

### User

The countries BR and DO will have the Users created with the following Accounts in microservice:

#### DO

- User created with email: **abiautotest+2@mailinator.com**, password: **Password1**, with Account ID **9883300001**
- User created with email: **abiautotest+100@mailinator.com**, password: **Pass()12**, with Account ID **9883300001** and **9883300003**
 

- User created with email: **abiautotest+1@gmail.com**, password: **Password1**, with Account ID **9883300002**, with phone **+5519992666528**
- User created with email: **abiautotest+2@gmail.com**, password: **Password1**, with Account ID **9883300002** and **9883300003**
- User created with email: **abiautotest+100@gmail.com**, password: **Pass()12**, with Account ID **9883300002** and **9883300003**


#### BR

- User created with email: **abiautotest+2@mailinator.com**, password: **Password1**, with Account ID **99481543000135** 
- User created with email: **abiautotest+100@mailinator.com**, password: **Pass()12**, with Account ID **99481543000135** and **42282891000166**


- User created with email: **abiautotest+1@gmail.com**, password: **Password1**, with Account ID **56338831000122** 
- User created with email: **abiautotest+2@gmail.com**, password: **Password1**, with Account ID **56338831000122** and **42282891000166**
- User created with email: **abiautotest+100@gmail.com**, password: **Pass()12**, with Account ID **56338831000122** and **42282891000166** 

#### AR

- User created with email: **abiautotest+2@mailinator.com**, password: **Password1**, with Account ID **5444385012** 
- User created with email: **abiautotest+100@mailinator.com**, password: **Pass()12**, with Account ID **5444385012** and **1669325565**


- User created with email: **abiautotest+1@gmail.com**, password: **Password1**, with Account ID **9932094352** 
- User created with email: **abiautotest+2@gmail.com**, password: **Password1**, with Account ID **9932094352** and **1669325565**
- User created with email: **abiautotest+100@gmail.com**, password: **Pass()12**, with Account ID **9932094352** and **1669325565** 

#### CL

- User created with email: **abiautotest+2@mailinator.com**, password: **Password1**, with Account ID **2323434554** 
- User created with email: **abiautotest+100@mailinator.com**, password: **Pass()12**, with Account ID **2323434554** and **3325534210**


- User created with email: **abiautotest+1@gmail.com**, password: **Password1**, with Account ID **1020303040** 
- User created with email: **abiautotest+2@gmail.com**, password: **Password1**, with Account ID **1020303040** and **3325534210**
- User created with email: **abiautotest+100@gmail.com**, password: **Pass()12**, with Account ID **1020303040** and **3325534210** 

#### ZA

- User created with email: **abiautotest+2@mailinator.com**, password: **Password1**, with Account ID **9883300101** 
- User created with email: **abiautotest+100@mailinator.com**, password: **Pass()12**, with Account ID **9883300101** and **9883300103**


- User created with email: **abiautotest+1@gmail.com**, password: **Password1**, with Account ID **9883300102** 
- User created with email: **abiautotest+2@gmail.com**, password: **Password1**, with Account ID **9883300102** and **9883300103**
- User created with email: **abiautotest+100@gmail.com**, password: **Pass()12**, with Account ID **9883300102** and **9883300103** 


 
### Products

## All

Populates everything from the following options:

- Common
