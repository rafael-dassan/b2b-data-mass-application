# B2B Product - Mass Populator Script

This folder contains the Mass Populator Script, aimed to be called on Pipelines to ensure all data needed for test executions will be created accordingly.

## Running the Script

To launch the script, please follow the steps below after opening the Terminal:

```sh
cd <project-root-dir>/data-mass/
```

You could execute the script using 3 parameters:

```sh
python3 populate_mass.py <COUNTRY> <ENVIRONMENT> <EXECUTION_TYPE>
```

Example #1:

- Executing Mass Populator for:
  - Country: Dominican Republic
  - Environment: UAT
  - Tests Scenarios to Create Data: ALL (populate data for tests that are available for all countries)

```sh
python3 populate.py DO UAT all
```

Example #2:

- Executing Mass Populator for:
  - Country: Argentina
  - Environment: DEV
  - Tests Scenarios to Create Data: common (populate only data for tests that are common for all countries)

```sh
python3 populate.py AR DEV common
```

Example #3:

- Executing Mass Populator for:
  - Country: Dominican Republic
  - Environment: SIT
  - Tests Scenarios to validate populator script: test (In this special case, to make sure all core components (recommendation, user, account) are working as expected)

```sh
python3 populate.py DO SIT test
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

2) Country BR hasn’t file category.csv, so will be populated standard file. 

``` 
📦data
 ┣ 📂ar
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┣ 📂br
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┣ 📂cl
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜product.csv
 ┃ ┗ 📜user.csv
 ┣ 📂co
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┣ 📂do
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┣ 📂za
 ┃ ┣ 📜account.csv
 ┃ ┣ 📜product.csv
 ┃ ┣ 📜recommendation.csv
 ┃ ┗ 📜user.csv
 ┗ 📜category.csv
 ┗ 📜account.csv
```

Notes: 

1) It's important to check file data-mass/mass-populator/common.py if country you want to populate some data has permissions to do that.

2) To create products on file product.csv the column named 'name' should contains as substring: [ANDROID, IOS or WEB]
This is not required, but it's needed to associate products to specific category properly.

Examples: 0101WEB, 0101ANDROID, 0101IOS 
