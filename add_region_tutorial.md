# Adding a new region on data_mass

## Add REDIRECT_URL and CLIENT_ID Parameters to the Functions that uses regions:
``` python
def get_iam_b2c_country_params_uat(country):     
def get_iam_b2c_country_params_sit(country):
def get_iam_b2c_country_params_qa(country):
```
## For example:
```python
params = { "NEW_REGION": {  
    "REDIRECT_URL": "$url",
    "CLIENT_ID": "$id" }}
```
## Also add the new region to the validation.py file
``` python
def valid_country(country):
    switcher = {
        "NEW_REGION": True,
```