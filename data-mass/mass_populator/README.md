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
  - Tests Scenarios to Create Data: ALL

```sh
python3 populate.py DO UAT all
```

Example #2:

- Executing Mass Populator for:
  - Country: Argentina
  - Environment: DEV
  - Tests Scenarios to Create Data: common (only data for tests that are common for all countries)

```sh
python3 populate.py AR DEV common
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