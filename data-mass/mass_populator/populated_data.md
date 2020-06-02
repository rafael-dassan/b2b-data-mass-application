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
| CO | Colombia | Yes | No |

All accounts will have 100 products or the maximum available products for that country associated with them.

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

#### CO

- Account 1: created with ID **9883300201**, name **CO_POC_001**, payment method **[CASH]**, with liquor license, with delivery window, credit **41000**, balance **50100**.
- Account 2: created with ID **9883300202**, name **CO_POC_002**, payment method **[CREDIT]**, with liquor license, with delivery window, credit **42000**, balance **50200**.
- Account 3: created with ID **9883300203**, name **CO_POC_003**, payment method **[CASH, CREDIT]**, with liquor license, without delivery window, credit **43000**, balance **50300**.


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

#### CO

- User created with email: **abiautotest+2@mailinator.com**, password: **Password1**, with Account ID **9883300201**
- User created with email: **abiautotest+100@mailinator.com**, password: **Pass()12**, with Account ID **9883300201** and **9883300203**
 

- User created with email: **abiautotest+1@gmail.com**, password: **Password1**, with Account ID **9883300202**, with phone **+5519992666528**
- User created with email: **abiautotest+2@gmail.com**, password: **Password1**, with Account ID **9883300202** and **9883300203**
- User created with email: **abiautotest+100@gmail.com**, password: **Pass()12**, with Account ID **9883300202** and **9883300203** 


### Recommendations
The countries will have the recommendations described bellow.

#### Beer Recommender - [Quick Order, Forgotten Items, Sell Up]

##### BR

- Beer Recommender associated with POC **99481543000135** and POC **42282891000166**.

##### DO

- Beer Recommender associated with POC **9883300001** and POC **9883300003**.

##### ZA

- Beer Recommender associated with POC **9883300101** and POC **9883300103**.

##### CO

- Beer Recommender associated with POC **9883300201** and POC **9883300203**.

## All

Populates everything from the following options:

- Common

## Product

Populate products for all countries.

##### AR

|SKUIdentifier|ItemName     |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-------------|---------|-----------------------|----------|----------
|0101WEB      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2

##### BR

|SKUIdentifier|ItemName     |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-------------|---------|-----------------------|----------|----------
|0101WEB      |QM Journey 01|Journey  |Garrafa / 1000 / ML    |No        |1
|0101ANDROID  |QM Journey 01|Journey  |Garrafa / 1000 / ML    |No        |1
|0101IOS      |QM Journey 01|Journey  |Garrafa / 1000 / ML    |No        |1
|0102WEB      |QM Journey 02|Journey  |Garrafa / 1000 / ML    |No        |2
|0102ANDROID  |QM Journey 02|Journey  |Garrafa / 1000 / ML    |No        |2
|0102IOS      |QM Journey 02|Journey  |Garrafa / 1000 / ML    |No        |2

##### CO

|SKUIdentifier|ItemName     |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-------------|---------|-----------------------|----------|----------
|0101WEB      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2


##### CL

|SKUIdentifier|ItemName     |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-------------|---------|-----------------------|----------|----------
|0101WEB      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2


##### DO

|SKUIdentifier|ItemName     |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-------------|---------|-----------------------|----------|----------
|0101WEB      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QM Journey 01|Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QM Journey 02|Journey  |Botella / 1000 / ML    |No        |2


##### ZA

|SKUIdentifier|ItemName     |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-------------|---------|-----------------------|----------|----------
|0101WEB      |QM Journey 01|Journey  |Bottle / 1000 / ML     |Yes       |1
|0101ANDROID  |QM Journey 01|Journey  |Bottle / 1000 / ML     |Yes       |1
|0101IOS      |QM Journey 01|Journey  |Bottle / 1000 / ML     |Yes       |1
|0102WEB      |QM Journey 02|Journey  |Bottle / 1000 / ML     |Yes       |2
|0102ANDROID  |QM Journey 02|Journey  |Bottle / 1000 / ML     |Yes       |2
|0102IOS      |QM Journey 02|Journey  |Bottle / 1000 / ML     |Yes       |2