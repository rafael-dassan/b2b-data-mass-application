# B2B Product - Mass Populator Script

This folder contains the Mass Populator Script, aimed to be called on Pipelines to ensure all data needed for test executions will be created accordingly.

## Running the Script

To launch the script, please follow the steps below after opening the Terminal:

```sh
cd <project-root-dir>/data-mass/
```

You could execute the script using 3 parameters:

```sh
python3 populate.py <COUNTRY> <ENVIRONMENT> <EXECUTION_TYPE>
```

Example #1:

- Executing Mass Populator for:
  - Country: Dominican Republic
  - Environment: UAT
  - Execution type to populate data for tests that are available for all countries: `all`

```sh
python3 populate.py DO UAT all
```

Example #2:

- Executing Mass Populator for:
  - Country: Argentina
  - Environment: DEV
  - Execution type to populate data for tests that are common for all countries: `common`

```sh
python3 populate.py AR DEV common
```

Example #3:

- Executing Mass Populator for:
  - Country: Dominican Republic
  - Environment: SIT
  - Execution type to validate the populator script: `test`

```sh
python3 populate.py DO SIT test
```

Example #4:

- Executing Mass Populator for:
  - Country: Dominican Republic
  - Environment: SIT
  - Execution type to populate specific products for a specific country: `product`

```sh
python3 populate.py DO SIT product
```

## How to change Log Level

### INFO to DEBUG

```sh
sed -i 's/level=logging.INFO/level=logging.DEBUG/' log.py
```

### DEBUG to INFO

```sh
sed -i 's/level=logging.DEBUG/level=logging.INFO/' log.py
```

## Change data to populate

The data folder will provide all data information for populator script to use. On root level, the file contain standard data that can be used for all zones/countries, if it is needed specific data, the user can customize it for each country. In order to do that, create a file inside a country folder and this file will be used on populator instead of the standard one.

Each csv file contains information of a specific entity that populator currently support. The file format is defined in the header of each csv and must be used in this way for it to work. To add new data, include new lines following the header definition of data.

Example: 

1) We have file account.csv which belongs to data folder (standard folder), the country BR has a file account.csv, thereby its content will be used to populate instead of standard file account.py.

2) All countries have use the same category information, so it will be populated via standard file `category.csv`. 

``` 
📦data
 ┣ 📂ar
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┣ 📜rewards.csv
 ┃ ┗ 📜user.csv
 ┣ 📂br
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┣ 📜rewards.csv
 ┃ ┗ 📜user.csv
 ┣ 📂co
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┣ 📜rewards.csv
 ┃ ┗ 📜user.csv
 ┣ 📂do
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┣ 📜rewards.csv
 ┃ ┗ 📜user.csv
 ┣ 📂ec
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┣ 📂mx
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┣ 📜rewards.csv
 ┃ ┗ 📜user.csv
 ┣ 📂pe
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┣ 📂za
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜deal.csv
 ┃ ┣ 📜invoice.csv
 ┃ ┣ 📜order.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┣ 📜rewards.csv
 ┃ ┗ 📜user.csv
 ┗ 📜category.csv
```

Notes: 

1) It's important to check file data-mass/mass-populator/common.py if country you want to populate some data has permissions to do that.

2) To associate product to category, the algorithm uses substring from the product name to determine which category it belongs to. So, for a product to be associated to a category, when creating it on file product.csv the column 'name' should contain as substring one of the following: [ANDROID, IOS or WEB]
This is not required, but it's needed to associate products to mobile or web categories properly.

Examples: 0101WEB, 0101ANDROID, 0101IOS

## Troubleshooting - Create and enable products on Magento
Magento has a cache in its internal database that needs to be re-indexed after changes are made to Magento entities from scripts. This process is performed automatically in a few circumstances:
* Deploy the environment
* Success cron job execution *abinbev_combo_service_importer*
In practice, re-indexing can take days to complete.
In some scenarios, it may be that the re-indexing process is not effective, and needs to be done manually for the changes made to take effect. This can happen over system instability, environment configuration changes and it will impact the enabling of new products and their association with categories

## Troubleshooting - OTP parameters (OTP Secret and OTP Interval)
The OTP secret and interval should not change often, but in case it occurs, please perform the steps below:
* Go to the [platform-config](https://ab-inbev.visualstudio.com/GHQ_B2B_Delta/_git/platform-config) repository
* Go to `microservices/releases/contact-verification-service`
* Select the specific environment-values file to check the OTP parameters for [SIT](https://ab-inbev.visualstudio.com/GHQ_B2B_Delta/_git/platform-config?path=%2Fmicroservices%2Freleases%2Fcontact-verification-service%2Fcontact-verification-service-qa-values.yaml) and [UAT](https://ab-inbev.visualstudio.com/GHQ_B2B_Delta/_git/platform-config?path=%2Fmicroservices%2Freleases%2Fcontact-verification-service%2Fcontact-verification-service-uat-values.yaml)
* Update the new values in [data-mass/user_creation_v3.py](../../data-mass/user_creation_v3.py)
