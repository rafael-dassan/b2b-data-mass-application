# Populated Data

## Common

### Accounts

All countries will have the Accounts created using Accounts Microservice.

Only ZA has also the two Accounts created for Microservice and Middleware (check the table below).

| Country Code | Country Name | Microservice | Middleware |
|:-----------:|:-----------:|:-----------:|:-----------:|
| AR | Argentina | Yes | Yes |
| BR | Brazil | Yes | No |
| CL | Chile | Yes | No |
| DO | Dominican Republic | Yes | No |
| ZA | South Africa | Yes | No |
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

Accounts list:
| Name | Id |
| --- | --- |
| account_id_poc_1 | 9883300001 |
| account_id_poc_2 | 9883300002 |
| account_id_poc_3 | 9883300003 |

- User created with email: **qm.team.do+222@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.do+333@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.do+10000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_1,account_id_poc_3]**

- User created with email: **qm.team.do+1@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.do+2@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.do+3@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.do+100@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

- User created with email: **qm.team.do+11@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.do+22@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.do+33@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.do+1000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

#### BR

Accounts list:
| Name | Id |
| --- | --- |
| account_id_poc_1 | 99481543000135 |
| account_id_poc_2 | 56338831000122 |
| account_id_poc_3 | 42282891000166 |

- User created with email: **qm.team.br+222@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.br+333@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.br+10000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_1,account_id_poc_3]**

- User created with email: **qm.team.br+1@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.br+2@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.br+3@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.br+100@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

- User created with email: **qm.team.br+11@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.br+22@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.br+33@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.br+1000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

#### AR

Accounts list:
| Name | Id |
| --- | --- |
| account_id_poc_1 | 5444385012 |
| account_id_poc_2 | 9932094352 |
| account_id_poc_3 | 1669325565 |

- User created with email: **qm.team.ar+222@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.ar+333@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.ar+10000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_1,account_id_poc_3]**

- User created with email: **qm.team.ar+1@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.ar+2@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.ar+3@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.ar+100@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

- User created with email: **qm.team.ar+11@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.ar+22@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.ar+33@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.ar+1000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]** 

#### CL

Accounts list:
| Name | Id |
| --- | --- |
| account_id_poc_1 | 2323434554 |
| account_id_poc_2 | 1020303040 |
| account_id_poc_3 | 3325534210 |

- User created with email: **qm.team.cl+222@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.cl+333@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.cl+10000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_1,account_id_poc_3]**

- User created with email: **qm.team.cl+1@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.cl+2@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.cl+3@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.cl+100@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

- User created with email: **qm.team.cl+11@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.cl+22@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.cl+33@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.cl+1000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

#### ZA

Accounts list:
| Name | Id |
| --- | --- |
| account_id_poc_1 | 9883300101 |
| account_id_poc_2 | 9883300102 |
| account_id_poc_3 | 9883300103 |

- User created with email: **qm.team.za+222@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.za+333@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.za+10000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_1,account_id_poc_3]**

- User created with email: **qm.team.za+1@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.za+2@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.za+3@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.za+100@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

- User created with email: **qm.team.za+11@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.za+22@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.za+33@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.za+1000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

#### CO

Accounts list:
| Name | Id |
| --- | --- |
| account_id_poc_1 | 9883300201 |
| account_id_poc_2 | 9883300202 |
| account_id_poc_3 | 9883300203 |

- User created with email: **qm.team.co+222@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.co+333@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.co+10000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_1,account_id_poc_3]**

- User created with email: **qm.team.co+1@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.co+2@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.co+3@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.co+100@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**

- User created with email: **qm.team.co+11@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.co+22@gmail.com**, password: **Password1**, with Account **[account_id_poc_2,account_id_poc_3]**
- User created with email: **qm.team.co+33@gmail.com**, password: **Password1**, with Account **[account_id_poc_1]**
- User created with email: **qm.team.co+1000@gmail.com**, password: **Pass()12**, with Account **[account_id_poc_2,account_id_poc_3]**


### Recommendations
The countries will have the recommendations described bellow.

#### Beer Recommender - [Quick Order, Forgotten Items]

##### AR

- Beer Recommender associated with POC **5444385012** and POC **9932094352**.

##### BR

- Beer Recommender associated with POC **99481543000135** and POC **56338831000122**.

##### DO

- Beer Recommender associated with POC **9883300001** and POC **9883300002**.

##### ZA

- Beer Recommender associated with POC **9883300101** and POC **9883300102**.

##### CO

- Beer Recommender associated with POC **9883300201** and POC **9883300202**.


## All

Populates everything from the following options:

- Common

## Product

Populate products for all countries.

##### AR

|SKUIdentifier|ItemName   |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-----------|---------|-----------------------|----------|----------
|0101WEB      |QMWEB01    |Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QMANDROID01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QMIOS01    |Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QMWEB02    |Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QMANDROID02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QMIOS02    |Journey  |Botella / 1000 / ML    |No        |2

##### BR

|SKUIdentifier|ItemName   |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-----------|---------|-----------------------|----------|----------
|0101WEB      |QMWEB01    |Journey  |Garrafa / 1000 / ML    |No        |1
|0101ANDROID  |QMANDROID01|Journey  |Garrafa / 1000 / ML    |No        |1
|0101IOS      |QMIOS01    |Journey  |Garrafa / 1000 / ML    |No        |1
|0102WEB      |QMWEB02    |Journey  |Garrafa / 1000 / ML    |No        |2
|0102ANDROID  |QMANDROID02|Journey  |Garrafa / 1000 / ML    |No        |2
|0102IOS      |QMIOS02    |Journey  |Garrafa / 1000 / ML    |No        |2

##### CO

|SKUIdentifier|ItemName   |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-----------|---------|-----------------------|----------|----------
|0101WEB      |QMWEB01    |Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QMANDROID01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QMIOS01    |Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QMWEB02    |Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QMANDROID02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QMIOS02    |Journey  |Botella / 1000 / ML    |No        |2

##### CL

|SKUIdentifier|ItemName   |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-----------|---------|-----------------------|----------|----------
|0101WEB      |QMWEB01    |Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QMANDROID01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QMIOS01    |Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QMWEB02    |Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QMANDROID02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QMIOS02    |Journey  |Botella / 1000 / ML    |No        |2

##### DO

|SKUIdentifier|ItemName   |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-----------|---------|-----------------------|----------|----------
|0101WEB      |QMWEB01    |Journey  |Botella / 1000 / ML    |No        |1
|0101ANDROID  |QMANDROID01|Journey  |Botella / 1000 / ML    |No        |1
|0101IOS      |QMIOS01    |Journey  |Botella / 1000 / ML    |No        |1
|0102WEB      |QMWEB02    |Journey  |Botella / 1000 / ML    |No        |2
|0102ANDROID  |QMANDROID02|Journey  |Botella / 1000 / ML    |No        |2
|0102IOS      |QMIOS02    |Journey  |Botella / 1000 / ML    |No        |2

##### ZA

|SKUIdentifier|ItemName   |BrandName|ContainerName/Size/Unit|Returnable|SalesRanking
|-------------|-----------|---------|-----------------------|----------|----------
|0101WEB      |QMWEB01    |Journey  |Bottle / 1000 / ML     |Yes       |1
|0101ANDROID  |QMANDROID01|Journey  |Bottle / 1000 / ML     |Yes       |1
|0101IOS      |QMIOS01    |Journey  |Bottle / 1000 / ML     |Yes       |1
|0102WEB      |QMWEB02    |Journey  |Bottle / 1000 / ML     |Yes       |2
|0102ANDROID  |QMANDROID02|Journey  |Bottle / 1000 / ML     |Yes       |2
|0102IOS      |QMIOS02    |Journey  |Bottle / 1000 / ML     |Yes       |2


### Category

The countries will have the categories created with the following products:
All products should be enabled and associated to accordingly categories 

#### DO

|SKUIdentifier|CategoryName|CategoryParent
|-------------|------------|--------------
|0101WEB      |Journey     |Web
|0101ANDROID  |Journey     |Mobile
|0101IOS      |Journey     |Mobile
|0102WEB      |Journey     |Web
|0102ANDROID  |Journey     |Mobile
|0102IOS      |Journey     |Mobile

#### AR

|SKUIdentifier|CategoryName|CategoryParent
|-------------|------------|--------------
|0101WEB      |Journey     |Web
|0101ANDROID  |Journey     |Mobile
|0101IOS      |Journey     |Mobile
|0102WEB      |Journey     |Web
|0102ANDROID  |Journey     |Mobile
|0102IOS      |Journey     |Mobile

#### BR

|SKUIdentifier|CategoryName|CategoryParent
|-------------|------------|--------------
|0101WEB      |Journey     |Web
|0101ANDROID  |Journey     |Mobile
|0101IOS      |Journey     |Mobile
|0102WEB      |Journey     |Web
|0102ANDROID  |Journey     |Mobile
|0102IOS      |Journey     |Mobile

#### CO

|SKUIdentifier|CategoryName|CategoryParent
|-------------|------------|--------------
|0101WEB      |Journey     |Web
|0101ANDROID  |Journey     |Mobile
|0101IOS      |Journey     |Mobile
|0102WEB      |Journey     |Web
|0102ANDROID  |Journey     |Mobile
|0102IOS      |Journey     |Mobile

#### ZA

|SKUIdentifier|CategoryName|CategoryParent
|-------------|------------|--------------
|0101WEB      |Journey     |Web
|0101ANDROID  |Journey     |Mobile
|0101IOS      |Journey     |Mobile
|0102WEB      |Journey     |Web
|0102ANDROID  |Journey     |Mobile
|0102IOS      |Journey     |Mobile


## Troubleshooting - Create and enable products on Magento
Magento has a cache in its internal database that needs to be re-indexed after changes are made to Magento entities from scripts. This process is performed automatically in a few circumstances:
* Deploy the environment
* Success cron job execution *abinbev_combo_service_importer*
In practice, re-indexing can take days to complete.
In some scenarios, it may be that the re-indexing process is not effective, and needs to be done manually for the changes made to take effect. This can happen over system instability, environment configuration changes and it will impact the enabling of new products and their association with categories.
